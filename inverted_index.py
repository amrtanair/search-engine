import requests
import re
import math
from bs4 import BeautifulSoup
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
import numpy as np
from sklearn import preprocessing
from sklearn.metrics.pairwise import cosine_similarity
stop_words = set(stopwords.words('english'))

def fetch_soup(url):
    request = requests.get(url)
    soup = BeautifulSoup(request.text, 'html.parser')

    for script in soup(["script", "style", "\n"]):
        script.decompose()
    text = soup.get_text()
    return text

def tokenize(text):
    word_tokens = word_tokenize(text)
    title=re.sub('[^A-Za-z0-9 ]+', "", text)

    tokens = [] # index for hash
    document = [] # text of page in array format

    for w in word_tokens: 
        if w.isalpha(): 
            document.append(w.lower())
            if w.lower() not in stop_words:
                tokens.append(w.lower())

    return tokens, document

def normalize(vector):
    X = np.asarray(vector, dtype=np.float).reshape(-1,1)
    X_normalized = preprocessing.normalize(X, norm='l2')
    return X_normalized

def generate_inverted_index(url):
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
    for key in child_inverted_index:
        if key not in mother_inverted_index.keys():
            mother_inverted_index[key] = [[doc_id, child_inverted_index[key]]]
            df[key] = 1
        else:
            mother_inverted_index[key].append([doc_id, child_inverted_index[key]])
            df[key] = df[key] + 1
    return mother_inverted_index, df

def compute_idf(df, size):
    for key in df.keys():
        df[key] = math.log((size+1)/df[key]) + 1
    return df

def compute_tfidf(tf, idf):
    tfidf_hash = [] # list of hashes(list of tfidf for every word in every doc)
    tfidf = []
    for i, doc in enumerate(tf):
        tfidfi = {}
        for key in idf:
            if key not in doc.keys():
                tfidfi[key] = 0
            else:
                tfidfi[key] = idf[key] * doc[key]
        tfidf_hash.append(tfidfi)

    for i in tfidf_hash:
        k = normalize(list(i.values()))
        tfidf.append(k)
    return tfidf

def driver(urls):
    mother_inverted_index = {}
    df = {} # document frequency
    tf = [] # term frequency
    for i,url in enumerate(urls):
        inverted_index, tfi = generate_inverted_index(url)
        mother_inverted_index, df = merge_inverted_index(inverted_index, mother_inverted_index, df, i)
        tf.append(tfi)
    idf = compute_idf(df, len(urls))
    tfidf = compute_tfidf(tf, idf)

    map_tfidf_url = {}
    for (key, url) in zip(tfidf, urls):
        map_tfidf_url[url] = key
    return mother_inverted_index, idf, map_tfidf_url

