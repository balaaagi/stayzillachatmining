from __future__ import division
from nltk import word_tokenize
from nltk.corpus import wordnet as wn
import csv
import nltk


message=[]
tags=['hotel','stay','trip','travel','room','resort','book','price','accomodation','cost','price','suite','tour','home stay']
data={}

# sentence="hellow world this is an awesome world we have great hotel also i would like to stay there"

print "## Data Cleaning Going to Start##"

print "## Opened the File##"

for t in csv.DictReader(open('data/hackathon_chat_data.csv'),delimiter=","):



	sentence=str(t['Chat Message']).lower().decode("utf8","ignore")
	message_text=nltk.Text(sentence)
	data_tags=[]
	relevant_word=0
	for word in sentence.split():
		if word in tags:
			relevant_word=1
			if word not in data_tags:
				data_tags.append(word)

	if relevant_word==1:
		data['message']=sentence
		data['tag']=data_tags
		print  data 
		
