from __future__ import division
from nltk import word_tokenize
from nltk.corpus import wordnet as wn
import csv
import nltk
import datetime
import re, collections
import pymongo
from pymongo import MongoClient
import codecs


message=[]
tags=['hotel','stay','trip','travel','room','resort','book','price','accomodation','cost','price','suite','tour','home stay','accom']




# MongoDB Connection
client=MongoClient('localhost', 27017)
# Connecting to DataBase
db=client.chat_logs
# Connection to the collections
# chat=db.cleaned_chats


## Spell Checker For Validating the spelling from http://norvig.com/spell-correct.html begins
def words(text): return re.findall('[a-z]+', text.lower()) 

def train(features):
    model = collections.defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    return model

NWORDS = train(words(file('data/big.txt').read()))

alphabet = 'abcdefghijklmnopqrstuvwxyz'

def edits1(word):
   splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
   deletes    = [a + b[1:] for a, b in splits if b]
   transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
   replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
   inserts    = [a + c + b     for a, b in splits for c in alphabet]
   return set(deletes + transposes + replaces + inserts)

def known_edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

def known(words): return set(w for w in words if w in NWORDS)

def correct(word):
    candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]
    return max(candidates, key=NWORDS.get)
## Spell Checker For Validating the spelling from http://norvig.com/spell-correct.html ends

# My own function to get the city code from city code context
def getcityCode(city_context):
	city_context_array=city_context.split(':')
	if len(city_context_array[0].strip())>10 and city_context_array[0].isdigit():
		return int(city_context_array[0])
	else:
		return -1
		


print "## Data Cleaning Going to Start##"

print "## Opened the File##"

print "##Started Cleaning the file....."
for t in csv.DictReader(open('data/hackathon_chat_data.csv'),delimiter=","):


	print "..."
	sentence=str(t['Chat Message']).lower().decode("utf8","ignore")
	message_text=nltk.Text(sentence)
	data={}
	data_tags=[]
	relevant_word=0
	for word in sentence.split():
		# corrected_word=correct(word)
		if word in tags:
			relevant_word=1
			if word not in data_tags:
				data_tags.append(str(word))
		else:
			corrected_word=correct(word)
			if corrected_word in tags:
				relevant_word=1
				if corrected_word not in data_tags:
					data_tags.append(str(corrected_word))
				

	if relevant_word==1:
		try:
			data['timestamp']=datetime.datetime.fromtimestamp(int(str(t['UNIX Time Stamp']))).strftime('%Y-%m-%d %H:%M:%S')
		except Exception, e:
			data['timestamp']=datetime.datetime.fromtimestamp(int(str("00000000"))).strftime('%Y-%m-%d')
	    
		

		data['message']=str(sentence).encode('utf-8')
		data['tag']=data_tags
		data['chat_city']=getcityCode(str(t['chat_location_context']))
		# print data
		# Insert the json data into MongoDB
		db.cleaned_chats.insert(data) 



print "Successfully Cleaned the Data"
		
