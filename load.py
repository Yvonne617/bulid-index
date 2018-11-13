# encoding: utf-8
import requests,json,urllib
import nltk
nltk.download('punkt')
import sys
#define put method
def put(url,data):
 	headers = {'Content-type': 'application/json'}
	r = requests.put(url, data = json.dumps(data), headers = headers)
#define patch method
def patch(url,data):
	headers = {'Content-type':'application/json'}
	r = requests.patch(url,data = json.dumps(data),headers = headers)
#define get method
def get(url,data):
	headers = {'Content-type':'application/json'}
	r = requests.get(url,data = json.dumps(data),headers = headers)
	return r
#open prize.json file
script,filename = sys.argv 
with open(filename, 'r') as f:
    data = json.load(f)

#define firebase url
url = 'https://ing551hw1.firebaseio.com/.json'
# upload prizes data into firebase
put(url,data)
#create index node
indexNode = {'index':''}
patch(url, indexNode)


i = 0
k = 0
#put every id-motivation pair into a list
temp_motivations = []
i_len = len(data['prizes'])
for i in range (i_len):
	num = len(data['prizes'][i]['laureates'])
	for k in range (num):		
		m = data['prizes'][i]['laureates'][k]
		if (not('motivation' in m)) :  #ignore nodes which do not have motivation attribute
			continue
		m2 = m['motivation'].encode('utf-8')
		temp_motivations.append([m['id'],m2.lstrip('\"').rstrip('\"').replace('-',' ')]) 

#omit the repeated records
motivations = []
for i in temp_motivations:
    if i not in motivations:
        motivations.append(i)

#deal with stopwords and other symbols
f = open("stopwords.txt","r") 
lines = f.readlines()  #read file content
stop_words = []
for i in range(0,len(lines),1):
	stop_words.append(lines[i].rstrip('\n'))

my_dict = {} #define a dict to store results
for i in motivations:
	word_tokens = nltk.word_tokenize(i[1])
	word_tokens = [w.lower() for w in word_tokens] #lower all words
	word_tokens = [w for w in word_tokens if not w in stop_words] 
  	for w in word_tokens: 
    		if w not in stop_words and len(w)!=1 and w not in ['<I>','</I>','/i','\"','\'','"',"''",'\'s']:
    			if not my_dict.has_key(w): #create key if not exists
    				my_dict[w] = [i[0]]
    			else:
    				my_dict[w].append(i[0]) #append new id into id list if key exist
    		
url2 = 'https://ing551hw1.firebaseio.com/index.json'
put(url2,my_dict)  #create an inverted index