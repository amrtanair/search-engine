from inverted_index import normalize
from scipy import spatial

def query_vector(words, idf):
	# normalize and create k-dimensional query vector, 'k' being the number of terms in corpus
	qv = [0]*len(idf)
	i = 0
	for key in idf:
		if key not in words:
			i+=1
		else:
			qv[i] = idf[key]

	qv = normalize(qv)
	return qv

def get_relevant_urls(words, mother_inverted_index, urls):
	# fetch urls that contain the words in the query
	result= set()
	for elem in words:
		if elem not in mother_inverted_index:
			continue
		else:
			for i in range(len(mother_inverted_index[elem])):
				result.add(urls[mother_inverted_index[elem][i][0]])
	return result

def get_ranking(result, map_tfidf_url, qv):
	# compare similarity of docs to query vector using cosine similarity
	ranked_docs = {}
	for i, url in enumerate(result):
		v1 = map_tfidf_url[url]
		cs = 1 - spatial.distance.cosine(v1, qv)
		ranked_docs[url] = cs
	return ranked_docs
