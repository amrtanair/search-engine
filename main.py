# import pdb; pdb.set_trace()
from inverted_index import *

urls= ['https://harrypotter.fandom.com/wiki/Harry_Potter_and_the_Philosopher%27s_Stone', 
       # 'https://harrypotter.fandom.com/wiki/Harry_Potter_and_the_Chamber_of_Secrets', 
       # 'https://harrypotter.fandom.com/wiki/Harry_Potter_and_the_Prisoner_of_Azkaban', 
       # 'https://harrypotter.fandom.com/wiki/Harry_Potter_and_the_Goblet_of_Fire',
       'https://supernatural.fandom.com/wiki/Dean_Winchester',
       'https://supernatural.fandom.com/wiki/Sam_Winchester',
       # 'https://www.tutorialspoint.com/ruby-on-rails/rails-scaffolding.htm',
       'https://en.wikipedia.org/wiki/Facebook',
       'https://en.wikipedia.org/wiki/Anchovy',
       'https://en.wikipedia.org/wiki/Hungary']

mother_inverted_index, idf = driver(urls)
print("harry idf is", idf['harry'])
query = input("Enter query: ")
result=[]
position = []

words=query.split()
for elem in words:
	if elem not in mother_inverted_index.keys():
		continue
	else:
		for i in range(len(mother_inverted_index[elem])):
			position.append([elem, mother_inverted_index[elem]])
			result.append(urls[mother_inverted_index[elem][i][0]])

unique_list = (list(set(result))) 
print(unique_list)

