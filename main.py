from inverted_index import *
from query import *

# corpus
urls= [
		'https://harrypotter.fandom.com/wiki/Harry_Potter_and_the_Philosopher%27s_Stone', 
       'https://harrypotter.fandom.com/wiki/Harry_Potter_and_the_Chamber_of_Secrets', 
       'https://harrypotter.fandom.com/wiki/Harry_Potter_and_the_Prisoner_of_Azkaban', 
       'https://harrypotter.fandom.com/wiki/Harry_Potter_and_the_Goblet_of_Fire',
       'https://supernatural.fandom.com/wiki/Dean_Winchester',
       'https://supernatural.fandom.com/wiki/Sam_Winchester',
       'https://www.tutorialspoint.com/ruby-on-rails/rails-scaffolding.htm',
       'https://en.wikipedia.org/wiki/Facebook',
       'https://en.wikipedia.org/wiki/Anchovy',
       'https://en.wikipedia.org/wiki/Hungary'
       ]

query = input("Enter query: ")
# create list of query words in lowercase
words = [word.lower() for word in query.split()]

# inverted index for the corpus, inverse document frequency for every term in corpus and
# tfidf of each term mapped to its document
inverted_index, idf, map_tfidf_url = main(urls)

# normalize and create k-dimensional query vector, 'k' being the number of terms in corpus
qv = query_vector(words, idf)

# gets docs relevant to given query
result = get_relevant_urls(words, inverted_index, urls)

# rank docs using cosine similarity
ranking = get_ranking(result, map_tfidf_url, qv)

# list of relevant docs alongwith cosine similarity value.
# higher the value, higher the similarity
print(ranking)
