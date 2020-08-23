import requests
import re
import math
from bs4 import BeautifulSoup
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
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

def generate_inverted_index(url, doc_id, tf):
    text = fetch_soup(url)
    tokens, document = tokenize(text)
    inverted_index = {}

    for i,elem in enumerate(document):
        if elem not in tokens:
            continue
        else:
            if elem not in inverted_index.keys():
                inverted_index[elem]=[i]
            else:
                inverted_index[elem].append(i)
        
    return inverted_index

def merge_inverted_index(child_inverted_index, mother_inverted_index, df, doc_id):
    for key in child_inverted_index:
        if key not in mother_inverted_index.keys():
            mother_inverted_index[key] = [[doc_id, child_inverted_index[key]]]
            df[key] = 1
        else:
            mother_inverted_index[key].append([doc_id, child_inverted_index[key]])
            df[key] = df[key] + 1
    return mother_inverted_index, df

def compute_idf(df, y):
    for key in df:
        x = (y+1)/df[key]
        df[key] = math.log(x) + 1
    return df

def driver(urls):
    mother_inverted_index = {}
    df = {}
    tf = []
    for i,url in enumerate(urls):
        inverted_index = generate_inverted_index(url, i, tf)
        mother_inverted_index, df = merge_inverted_index(inverted_index, mother_inverted_index, df, i)
        print("harry df is", df['harry'])
    idf = compute_idf(df, len(urls))
    return mother_inverted_index, idf
