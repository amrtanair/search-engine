# Implement a search engine
This repository documents the process of implementing a search engine that takes a query term as an input and ranks relevant documents in the corpus. 
The corpus in this case is a collection of random documents, wiki's of a tv show's prominent characters, a movie franchise, a country, a social media company and a type of fish. 

## Breaking down the problem and the Approach

##### bare bones search engine
The first step was to create the inverted index(a dictionary that stores the mapping of a term to its occurences in a document/corpus) for a single document. This involved using the Requests library to fetch the contents of a webpage and the BeautifulSoup library to parse and store the text content on the webpage. The resulting textfile was then stored as tokens(a list that contains all words in the document(minus the stopwords) in lowercase format) and a document list. Later, the ivnverted index was created using the python dictionary data type. 

The second step was doing the same or a corpus, that is, creating an inverted index that included the position of every relevant term in every document. The way to do this was to create a ```mother_inverted_index``` that would be a collection of all inverted indexes such that the value for every key in the dictionary is a list of lists, something like this: 
Let's say the word "harry", appears in documents 1, 3, but not 2. The record in the hashmap would be as follows: 
```
'harry' => [[1, [45, 67, 54]], [2, [2, 5, 4]]]]
```
Every time the inverted index for a doc was created, it was 'merged' into the mother inverted index by looping through every term in the newly created one: adding the term to the larger inverted index if it doesn't exist and if it does exist, adding it to the existing key/value pair in the ```mother_inverted_index```.

The next step was the create a basic search engine, sans the ranking. A string was taken as an input and each individual word was compared with the inverted index. 
Next is : Ranking the documents. 

##### Ranking
For this, I used [tf-idf](https://en.wikipedia.org/wiki/Tf%E2%80%93idf) which is a term in statistics that basically describes how 'important' a term is in a given corpus. The easisest example would be to consider the following case:  




### Work ahead
