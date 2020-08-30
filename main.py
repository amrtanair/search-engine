# import pdb; pdb.set_trace()
from inverted_index import *

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

def query_vector(words, idf):
	qv = [0]*len(idf)
	i = 0
	for key in idf:
		if key not in words:
			i+=1
		else:
			qv[i] = idf[key]
	return qv

def get_relevant_urls(words, mother_inverted_index):
	result= set()
	position = []
	for elem in words:
		if elem not in mother_inverted_index.keys():
			continue
		else:
			for i in range(len(mother_inverted_index[elem])):
				position.append([elem, mother_inverted_index[elem]])
				result.add(urls[mother_inverted_index[elem][i][0]])
	return result

query = input("Enter query: ")
mother_inverted_index, idf, map_tfidf_url = driver(urls)
words=query.split()
urls = get_relevant_urls(words, mother_inverted_index)
qv = query_vector(words, idf)
n_qv = normalize(qv)
import pdb; pdb.set_trace()
