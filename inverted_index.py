import requests
import math
from bs4 import BeautifulSoup
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
import numpy as np
from scipy import spatial
from sklearn import preprocessing
stop_words = set(stopwords.words('english'))

def fetch_soup(url):
    # fetches the soup for a url and scrapes all js content
    request = requests.get(url)
    soup = BeautifulSoup(request.text, 'html.parser')

    for script in soup(["script", "style", "\n"]):
        script.decompose()
    text = soup.get_text()
    return text

def tokenize(text):
    # creates tokens and cleans the document(removes non-alphabetical 
    # material and converts words to lower case)
    word_tokens = word_tokenize(text)

    tokens = [] # index for hash
    document = [] # text of page in array format

    for w in word_tokens: 
        if w.isalpha(): 
            document.append(w.lower())
            if w.lower() not in stop_words:
                tokens.append(w.lower())

    return tokens, document

def normalize(vector):
    # reshapes vector and normalizes using l2 norm
    X = np.asarray(vector, dtype=np.float).reshape(-1,1)
    vector_normalized = preprocessing.normalize(X, norm='l2')

    return vector_normalized

def generate_inverted_index(url):
    # generates a dictionary that maps term to their occurences
    text = fetch_soup(url)
    tokens, document = tokenize(text)
    inverted_index = {}
    tf = {}

    for i,elem in enumerate(document):
        if elem not in tokens:
            continue
        else:
            if elem not in inverted_index.keys():
                inverted_index[elem]=[i]
                tf[elem] = 1
            else:
                inverted_index[elem].append(i)
                tf[elem] = tf[elem] + 1
    return inverted_index, tf

def merge_inverted_index(child_inverted_index, mother_inverted_index, df, doc_id):
    # combines inverted index of every doc to the inverted index for the corpus.
    # also keeps track of document frequency
    for key in child_inverted_index:
        if key not in mother_inverted_index.keys():
            mother_inverted_index[key] = [[doc_id, child_inverted_index[key]]]
            df[key] = 1
        else:
            mother_inverted_index[key].append([doc_id, child_inverted_index[key]])
            df[key] = df[key] + 1
    return mother_inverted_index, df

def compute_idf(df, size):
    # computes idf using the formula used by the scikit learn library
    for key in df.keys():
        df[key] = math.log((size+1)/df[key]) + 1
    return df

def compute_tfidf(tf, idf):
    # tf, idf is a dictionary
    # tfidf will be a lists of lists. each list will be the tfidf of every term in every doc.
    # tfidfi(i'th element of tfidf) will be k-dimensional.

    # we loop through every doc in the corpus and inside that loop we go through every term
    tfidf = []
    for i, doc in enumerate(tf):
        tfidfi = [0]*len(idf)
        i = 0
        for key in idf:
            if key not in doc:
                i = i + 1
            else:
                tfidfi[i] = idf[key] * doc[key]
        tfidf.append(normalize(tfidfi))

    return tfidf

def map_tfidf_to_urls(tfidf, urls):
    # the map_tfidf_url function maps the tfidf of each term in each doc(which is a dictionary) to the url 
    map_tfidf_url = {}
    for (key, url) in zip(tfidf, urls):
        map_tfidf_url[url] = key

    return map_tfidf_url

def main(urls):
    # mother inverted index is the index containing all terms in the corpus as keys and
    # the values being the doc_id and the 
    # position of occurence

    # df is a dictionary: the document frequency of each term. The dictionary is the same 
    # length as the mother inverted index, i.e,
    # it is k-dimensional where K is the total number of distinct terms

    # tf is a list: the term frequency of each term in each doc.

    # idf is the inverse document frequency

    mother_inverted_index = {}
    df = {} 
    tf = []

    for i,url in enumerate(urls):
        inverted_index, tfi = generate_inverted_index(url)
        mother_inverted_index, df = merge_inverted_index(inverted_index, mother_inverted_index, df, i)
        tf.append(tfi)

    idf = compute_idf(df, len(urls))
    tfidf = compute_tfidf(tf, idf)
    map_tfidf_url = map_tfidf_to_urls(tfidf, urls)

    return mother_inverted_index, idf, map_tfidf_url

