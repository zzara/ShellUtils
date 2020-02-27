#!/bin/env python3
# tolkein - web tokenizer
# v0.01a

import codecs
import nltk
import sys
import bs4
import urllib.request

def request_maker(url):
    tolkein_url = str(url)
    tolkein_headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}
    tolkein_req = urllib.request.Request(tolkein_url, data=None, headers=tolkein_headers)
    tolkein_res = urllib.request.urlopen(tolkein_req)
    
    # Transform the document into a readability paper summary
    tolkein_content = tolkein_res.read()
    tags = ['h1','h2','h3','h4','h5','h6','h7','p','li']
    
    # Parse the HTML using BeautifulSoup
    soup = bs4.BeautifulSoup(tolkein_content,'lxml')

    # Extract the paragraph delimiting elements
    for element in soup.find_all(tags):
        # Get the HTML node text
        paragraph = element.get_text()
       
        # Sentence Tokenize
        sentences = nltk.sent_tokenize(paragraph)
        for idx, sentence in enumerate(sentences):
            # Word Tokenize and Part of Speech Tagging
            sentences[idx] = nltk.pos_tag(nltk.word_tokenize(sentence))
    
        # Yield a list of sentences (the paragraph); each sentence of
        # which is a list of tuples in the form (token, tag).
        yield sentences

def file_handler(file, url):
    with codecs.open(file, 'w+', encoding='utf-8') as f:

        # Write paragraphs double newline separated and sentences
        # separated by a single newline. Also write token/tag pairs.
        for paragraph in request_maker(url):
            for sentence in paragraph:
                f.write(" ".join("%s/%s" % (word, tag) for word, tag in sentence))
                f.write("\n")
                f.write("\n")
    f.close()

if __name__ == "__main__": # execute this as a program drectly. do not make available functions as standalone.
    file_handler('corp.txt', 'https://www.effectivelanguagelearning.com/language-guide/mandarin-chinese-language')
