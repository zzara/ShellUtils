# -*- coding: utf-8 -*-

import argparse
import email
import glob
import itertools
import logging
import re
import string

import bs4
import gensim
import nltk
import multiprocessing as mp


def get_logger(logger_name) -> logging.Logger:
    """Logging config loader.
    
    Arguments:
        logger_name {str} -- Name of the logger. Default should be __name__.
    
    Returns:
        logging.Logger -- Logger object.
    """
    logging.basicConfig(
        format="%(asctime)s:%(levelname)s:%(module)s:%(filename)s:%(funcName)s:%(message)s",
        level=logging.INFO,
    )
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    logger.propagate = False
    return logger


logger = get_logger(__name__)


class EmailParser:
    """Parses an email and extracts text as tokens
    """

    def __init__(self, eml, auto=True):
        self.eml = eml
        self.eml_tokens = list()
        self.raw_text = str()

        if auto:
            self.parse_email()
            self.text_tokenize()

    def __len__(self):
        return len(self.eml_tokens)

    def parse_email(self):
        """Search for the raw HTML source, then extract the text
        """
        payload_decoded = str()
        eml = email.message_from_string(self.eml)
        for part in eml.walk():
            maybe_decoded_payload = part.get_payload(decode=True)
            if maybe_decoded_payload is not None:
                if part.get_content_type() == "text/html":
                    try:
                        try:
                            payload_decoded = str(bytes.decode(maybe_decoded_payload, part.get_content_charset()))
                        except Exception as e:
                            logger.error(f"status=error when decoding email error={e}")
                        parsed = bs4.BeautifulSoup(payload_decoded, "html.parser")
                        self.raw_text = self.recurse_for_text(parsed)
                    except Exception as e:
                        logger.error(f"status=error when parsing email body error={e}")

    def text_tokenize(self):
        """Clean and tokenize email text
        """
        self.eml_tokens = self.extract_candidate_chunks(self.clean_string(self.raw_text))

    @staticmethod
    def recurse_for_text(parsed: bs4.BeautifulSoup) -> str:
        """Recurses child elements of a bs4 object and extracts plain text
        
        Arguments:
            parsed {bs4.BeautifulSoup} -- Parsed bs4 object
        
        Returns:
            str -- string of text from an email
        """

        tokenized = []

        def recursive_search(parsed):
            """Internal tag searcher
            
            Arguments:
                parsed {tag} -- bs4 tag
            """
            for child in parsed.children:
                if (
                    isinstance(child, bs4.element.Doctype)
                    or isinstance(child, bs4.Comment)
                    or child.parent.name
                    in ["script", "noscript", "style", "meta", "img"]
                    or child == "\n"
                    or child == "\r\n"
                    or child is None
                ):
                    continue
                elif isinstance(child, bs4.element.NavigableString):
                    tokenized.append(child.string)
                elif isinstance(child, bs4.element.Tag):
                    recursive_search(child)

        if parsed is not None:
            recursive_search(parsed)
        return str(" ".join(tokenized))


    @staticmethod
    def extract_candidate_chunks(page, grammar=r'KT: {(<JJ>* <NN.*>+ <IN>)? <JJ>* <NN.*>+}'):
        
        # exclude candidates that are stop words or entirely punctuation
        punct = set(string.punctuation)
        stop_words = set(nltk.corpus.stopwords.words('english'))
        # tokenize, POS-tag, and chunk using regular expressions
        chunker = nltk.chunk.regexp.RegexpParser(grammar)
        tagged_sents = nltk.pos_tag_sents(nltk.word_tokenize(sent) for sent in nltk.sent_tokenize(page))
        all_chunks = list(itertools.chain.from_iterable(nltk.chunk.tree2conlltags(chunker.parse(tagged_sent))
                                                        for tagged_sent in tagged_sents))

        # join constituent chunk words into a single chunked phrase
        #candidates = [' '.join(word for word, pos, chunk in group).lower()
        #              for key, group in itertools.groupby(all_chunks, lambda (word,pos,chunk): chunk != 'O') if key]
        candidates = [' '.join(word for word, pos, chunk in group).lower() for key, group in itertools.groupby(all_chunks, lambda term: term[-1] != 'O') if key]

        return [cand for cand in candidates
                if cand not in stop_words and not all(char in punct for char in cand)]

    @staticmethod
    def extract_candidate_words(page, good_tags=set(['JJ', 'JJR', 'JJS', 'NN', 'NNP', 'NNS', 'NNPS'])):

        # exclude candidates that are stop words or entirely punctuation
        punct = set(string.punctuation)
        stop_words = set(nltk.corpus.stopwords.words('english'))
        # tokenize and POS-tag words
        tagged_words = itertools.chain.from_iterable(nltk.pos_tag_sents(nltk.word_tokenize(sent)
                                                                        for sent in nltk.sent_tokenize(page)))
        # filter on certain POS tags and lowercase all words
        candidates = [word.lower() for word, tag in tagged_words
                    if tag in good_tags and word.lower() not in stop_words
                    and not all(char in punct for char in word)]

        return candidates

    def score_keyphrases_by_tfidf(self, candidates='chunks'):
        # extract candidates from each text in texts, either chunks or words
        if candidates == 'chunks':
            boc_texts = [self.extract_candidate_chunks(text) for text in [self.raw_text]]
        elif candidates == 'words':
            boc_texts =  [self.extract_candidate_words(text) for text in [self.raw_text]]
        # make gensim dictionary and corpus
        dictionary = gensim.corpora.Dictionary(boc_texts)
        corpus = [dictionary.doc2bow(boc_text) for boc_text in boc_texts]
        # transform corpus with tf*idf model
        tfidf = gensim.models.TfidfModel(corpus)
        corpus_tfidf = tfidf[corpus]
        
        return corpus_tfidf, dictionary

    @staticmethod
    def clean_string(text: str) -> str:
        """Clean a string to prepare for tokenization
        
        Arguments:
            text {str} -- Email body text string
        
        Returns:
            str -- Cleaned email body text string
        """
        text = text
        text = re.sub(r"\=[0-9a-fA-F][0-9a-fA-F]", " ", text)
        text = re.sub(r"\=\n", r"", text)
        text = re.sub(r"([0-9a-zA-Z])(\n)([0-9a-zA-Z])", r"\1\3", text)
        text = re.sub(r"(\s)(\n)(\s)", r"\1", text)
        text = re.sub(r"\\[rnt]", "", text)
        text = re.sub(r"\?\?\?\?[rnt]", "", text)
        text = re.sub(r"['<>|]", "", text)
        return str(text)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", "-p", action="store")
    argus = parser.parse_args()

    files = glob.glob(f"{argus.path}*html")

    pool = mp.Pool(mp.cpu_count())
    port_result_objects = []

    samples = 20
    count = 0
    for file in files:
        if count > samples:
            break
        count += 1

        raw_eml = open(file).read()

        port_result_objects.append(pool.apply_async(EmailParser, args=(raw_eml,)))
        
        #msg = EmailParser(raw_eml)
        #print(msg.raw_text)
        #print(msg.eml_tokens)
        
        #corpus_tfidf, dictionary = msg.score_keyphrases_by_tfidf()
        #for key, val in dictionary.token2id.items():
        #    print(key, val)

    pool.close()
    pool.join()

    # retreive results
    results = list(filter(lambda x: x is not None and len(x) > 0, [result.get() for result in port_result_objects]))

    for r in results:
        print(r.eml_tokens)
