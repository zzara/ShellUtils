# -*- coding: utf-8 -*-

"""This module is an email topic modeler.
   Feed this a directory with raw email data from microsoft (.eml)
"""

__version__ = "1.0.1"

import email
import glob
import logging
import multiprocessing as mp
import re
import unicodedata
from itertools import groupby
from unicodedata import category as unicat

import bs4
import nltk
from nltk import ne_chunk, pos_tag, sent_tokenize, wordpunct_tokenize
from nltk.chunk import tree2conlltags
from nltk.chunk.regexp import RegexpParser
from nltk.corpus import wordnet as wn
from nltk.probability import FreqDist
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.decomposition import NMF, LatentDirichletAllocation, TruncatedSVD
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline
import pyLDAvis.gensim

import gensim
from gensim import corpora

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

en_stop = set(nltk.corpus.stopwords.words('english'))

# Number of emails to process
samples = 5000

# Number of topics to generate
topic_num = 100

# Number of topic keywords/phrases in each topic
topic_terms = 9

# Normalize and Tokenize
class TextNormalizer(BaseEstimator, TransformerMixin):

    def __init__(self, language='english'):
        self.stopwords  = set(nltk.corpus.stopwords.words(language))
        self.lemmatizer = WordNetLemmatizer()

    def is_punct(self, token):
        return all(
            unicodedata.category(char).startswith('P') for char in token
        )

    def is_stopword(self, token):
        return token.lower() in self.stopwords

    def normalize(self, document):
        return [
            self.lemmatize(token, tag).lower()
            for sentence in document
            for (token, tag) in sentence
            if not self.is_punct(token) and not self.is_stopword(token)
            and 40 > len(token) > 1
            and token is not None and token is not ''
            and not (re.match(r"^[0-9]+$", token))
        ]

    def lemmatize(self, token, pos_tag):
        tag = {
            'N': wn.NOUN,
            'V': wn.VERB,
            'R': wn.ADV,
            'J': wn.ADJ
        }.get(pos_tag[0], wn.NOUN)

        return self.lemmatizer.lemmatize(token, tag)

    def fit(self, X, y=None):
        return self

    def transform(self, documents):
        return [
            self.normalize(document)
            for document in documents
        ]
        
# Cleaning and Iterating Through Documents
def sents(paragraph):
    for sentence in sent_tokenize(paragraph):
        yield sentence

def tokenize(paragraph):
    for sentence in sents(paragraph):
        yield pos_tag(wordpunct_tokenize(sentence))

def clean_string(text):
    if isinstance(text, list):
        txtstr = ' '.join(text)
    else:
        txtstr = text

    recleaned = re.sub(r"\=[0-9a-fA-F][0-9a-fA-F]", " ", txtstr)
    recleaned = re.sub(r"\=\n", r"", recleaned)
    recleaned = re.sub(r"([0-9a-zA-Z])(\n)([0-9a-zA-Z])", r"\1\3", recleaned)
    recleaned = re.sub(r"(\s)(\n)(\s)", r"\1", recleaned)
    recleaned = re.sub(r"\\[rnt]", "", recleaned)
    recleaned = re.sub(r"\?\?\?\?[rnt]", "", recleaned)
    recleaned = re.sub(r"['<>|]", "", recleaned)
    return str(recleaned)

def recurse_for_text(parsed):
    tokenized = []

    def recursive_search(parsed):
        for child in parsed.children:
            if (
                isinstance(child, bs4.element.Doctype)
                or isinstance(child, bs4.Comment)
                or child.parent.name in ["script", "noscript", "style", "meta", "img"]
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
    return str(' '.join(tokenized))

def parse_email(filename, count, subject=False):
    '''Parse text from bs4'''
    try:
        html = open(str(filename)).read()
        eml = email.message_from_string(html)
        for part in eml.walk():
            maybe_decoded_payload = part.get_payload(decode=True)
            #print(part.get_content_charset())
            if (maybe_decoded_payload is not None):
                if subject:
                    if part.get_content_type() == 'text/plain':
                        try:
                            str(bytes.decode(maybe_decoded_payload, part.get_content_charset()))
                            try:
                                subject = re.search(r"Subject:\s?(.*)\r?\n", payload_decoded)[1]
                            except:
                                subject = None
                            result = list(tokenize(subject))
                            print(f"{count}: {filename}")
                            return result
                        except:
                            payload_decoded = str(maybe_decoded_payload)
                            return payload_decoded
                elif part.get_content_type() == 'text/html':
                    #from = re.search(r"From:\s?(.*)\r?\n", eml4txt)[1]
                    payload_decoded = str()
                    try:
                        payload_decoded = str(bytes.decode(maybe_decoded_payload, part.get_content_charset()))
                    except Exception as e:
                        print(e)
                    parsed = bs4.BeautifulSoup(str(payload_decoded), "html.parser")
                    text = recurse_for_text(parsed)
                    result = list(tokenize(clean_string(text)))
                    print(f"{count}: {filename}")
                    print(result)
                    return result
    except Exception as e:
        print(e)
        pass

# Topic Generator
def identity(words):
    return words

class SklearnTopicModels(object):

    def __init__(self, n_topics=10, estimator='LSA'):
        """
        n_topics is the desired number of topics
        To use Latent Semantic Analysis, set estimator to 'LSA',
        To use Non-Negative Matrix Factorization, set estimator to 'NMF',
        otherwise, defaults to Latent Dirichlet Allocation ('LDA').
        """
        self.n_topics = n_topics

        if estimator == 'LSA':
            self.estimator = TruncatedSVD(n_components=self.n_topics)
        elif estimator == 'NMF':
            self.estimator = NMF(n_components=self.n_topics)
        else:
            self.estimator = LatentDirichletAllocation(n_topics=self.n_topics)

        self.model = Pipeline([
            ('norm', TextNormalizer()),
            ('tfidf', CountVectorizer(tokenizer=identity,
                                      preprocessor=None, lowercase=False)),
            ('model', self.estimator)
        ])


    def fit_transform(self, documents):
        self.model.fit_transform(documents)

        return self.model


    def get_topics(self, n=topic_terms):
        """
        n is the number of top terms to show for each topic
        """
        vectorizer = self.model.named_steps['tfidf']
        model = self.model.steps[-1][1]
        names = vectorizer.get_feature_names()
        topics = dict()

        for idx, topic in enumerate(model.components_):
            features = topic.argsort()[:-(n - 1): -1]
            tokens = [names[i] for i in features]
            topics[idx] = tokens

        return topics

# Keyphrase Extraction
GRAMMAR = r'KT: {(<JJ>* <NN.*>+ <IN>)? <JJ>* <NN.*>+}'

class KeyphraseExtractor(BaseEstimator, TransformerMixin):
    """
    Wraps a PickledCorpusReader consisting of pos-tagged documents.
    """
    def __init__(self, grammar=GRAMMAR):
        self.grammar = GRAMMAR
        self.chunker = RegexpParser(self.grammar)

    def normalize(self, sent):
        """
        Removes punctuation from a tokenized/tagged sentence and
        lowercases words.
        """
        is_punct = lambda word: all(unicat(char).startswith('P') for char in word)
        sent = filter(lambda t: not is_punct(t[0]), sent)
        sent = list(sent)
        if len(sent) == 2:
            sent = map(lambda t: (t[0].lower(), t[1]), [sent])
            sent = list(sent)
        else:
            sent = list()
        return sent

    def extract_keyphrases(self, document):
        """
        For a document, parse sentences using our chunker created by
        our grammar, converting the parse tree into a tagged sequence.
        Yields extracted phrases.
        """
        for sents in document:
            for sent in sents:
                sent = self.normalize(sent)
                if not sent: continue
                chunks = tree2conlltags(self.chunker.parse(sent))
                phrases = [
                    " ".join(word for word, pos, chunk in group).lower()
                    for key, group in groupby(
                        chunks, lambda term: term[-1] != 'O'
                    ) if key
                ]
                for phrase in phrases:
                    yield phrase

    def fit(self, documents, y=None):
        return self

    def transform(self, documents):
        for document in documents:
            yield list(self.extract_keyphrases(document))

# Entity Extractor
GOODTAGS = frozenset(['JJ','JJR','JJS','NN','NNP','NNS','NNPS'])
GOODLABELS = frozenset(['PERSON', 'ORGANIZATION', 'FACILITY', 'GPE', 'GSP'])

class EntityExtractor(BaseEstimator, TransformerMixin):
    def __init__(self, labels=GOODLABELS, **kwargs):
        self.labels = labels

    def get_entities(self, document):
        entities = []
        for sentence in document:
            trees = ne_chunk(sentence)
            for tree in trees:
                if hasattr(tree, 'label'):
                    if tree.label() in self.labels:
                        entities.append(
                            ' '.join([child[0].lower() for child in tree])
                            )
        return entities

    def fit(self, documents, labels=None):
        return self

    def transform(self, documents):
        for document in documents:
            yield self.get_entities(document)


if __name__ == "__main__":
    # Processing Batches
    path = 'emails/'
    files = glob.glob(f"{path}*html")

    pool = mp.Pool(mp.cpu_count())
    port_result_objects = []

    subject = False
    count = 0
    for file in files:
        count += 1
        port_result_objects.append(pool.apply_async(parse_email, args=(file, count, subject,)))

        if count > samples:
            break
    pool.close()
    pool.join()

    # Retreive Results
    documents = list(filter(lambda x: x is not None and len(x) > 0, [result.get() for result in port_result_objects]))
    print(documents)

    # Get Topics
    skmodel = SklearnTopicModels(n_topics=topic_num, estimator='LSA')

    skmodel.fit_transform(documents)
    topics = skmodel.get_topics()
    for topic, terms in topics.items():
        print("Topic #{}:".format(topic+1))
        print(terms)

    # Get Keyphrases
    phrase_extractor = KeyphraseExtractor()
    keyphrases = list(phrase_extractor.fit_transform(documents))
    print(keyphrases[0:])

    # Get Entities
    entity_extractor = EntityExtractor()
    entities = list(entity_extractor.fit_transform(documents))
    print(entities[0:])

    # Get Entity Topics
    passes = 10
    dictionary = corpora.Dictionary(entities)
    doc_term_matrix = [dictionary.doc2bow(doc) for doc in entities]
    Lda = gensim.models.ldamodel.LdaModel
    ldamodel = Lda(doc_term_matrix, num_topics=topic_num, id2word = dictionary, passes=passes, per_word_topics=True)

    # Print Data
    for topic in ldamodel.print_topics(num_topics=topic_num, num_words=topic_terms):
        print(topic)
    #print(ldamodel.print_topics(num_topics=topic_num, num_words=6))
    
    # Visualize Data
    pyLDAvis.enable_notebook()
    vis = pyLDAvis.gensim.prepare(ldamodel, doc_term_matrix, dictionary, sort_topics=False)
    vis
