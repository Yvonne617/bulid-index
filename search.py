# encoding: utf-8
import requests,json,urllib
import sys

result = set() #create a set to store results
script,keys = sys.argv  # get the input keys
keys = keys.split(' ')
for k in keys:
	k = k.lower() #not case-sensitive
	url = 'https://ing551hw1.firebaseio.com/index/'+k+'.json'
	r = requests.get(url)
	r = r.text.replace('[','')
	r = r.replace(']','')
	for k in r.split(','):
		if k != 'null':
			result.add(k.encode('utf-8'))
#if do not find keywords, give an information
if len(result) is 0:
	print("no such keywords :(")
else:
	print("list of ids of prizes:",result)