# -*- coding: utf-8 -*-
"""
    TwiBot
    ~~~~~~~~
    A twitter bot to analyse, classify, cluster and visualise twitter tweet locations.
"""

import time
from sqlite3 import dbapi2 as sqlite3
from hashlib import md5
from datetime import datetime
from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash, _app_ctx_stack, make_response
from werkzeug import check_password_hash, generate_password_hash
import sys
import urllib,json
import pprint
sys.path.append('/home/vidhisha/TwiBot/summarizer')
from lexrank import *
sys.path.append('/home/vidhisha/TwiBot/classification')
from fetch_alt import *
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
import re
from os import listdir
from os.path import join
# configuration
SECRET_KEY = 'pSQ9kwR9xhW4aGcl5x0IptIzqHQrcOWIOfGbeDC8fuE'
app = Flask(__name__)
app.config.from_object(__name__)


@app.route('/summary')
def summary():
    """Genertes summaries of trending tweets and renders them
    """
    path = "summarizer/textfiles/"
    l = listdir(path)
    all_summaries = []
    for x in l:
        f = open(join(path,x),"r")
        s = f.read()
        f.close()
        s=s.strip("\n")
        s=s.replace('\xe2','')
        s=s.replace('\"','')
        m = gen_lexrank_summary(s,100)
        print m
        text = ""
        for i in range(len(m)):
            text = text+" "+m[i]
        text=re.sub(r'[^\x00-\x7F]+','', text)
        tag = x.split(".")[0]
        all_summaries.append((tag,text))
        #messages.replace('0x80','')
    #unicode(messages,errors='ignore')
    print all_summaries
    messages = all_summaries
    #return render_template('timeline.html', messages=messages)		
    response = render_template('summary.html', messages=messages)
    #response.headers['Content-type'] = 'text/html'
    return response

@app.route('/classification')
def classification():
    """classifies tweets and renders"""
    messages = benchmark(MultinomialNB(alpha=.01))
    response = render_template('classification.html',messages=messages)
    return response

def file_read(file_name):
	file_path = 'textfiles/'+file_name+'.txt'
        content = open(file_path,'r').read()
	loc = re.findall('Location.*',content)
        locations = []
        for i in loc:
		locations.append(i[10:])
	return locations

def file_read_tweet(file_name):
	file_path = 'textfiles/'+file_name+'.txt'
        content = open(file_path,'r').read()
        loc = re.findall('Tweet.*',content)
        locations = []
        for i in loc:
		i = i[10:]
		i=re.sub(r'[^\x00-\x7F]+','',i)
                locations.append(i[10:])
        return locations
 
@app.route('/')
def main():
    return render_template('layout.html')



@app.route('/visualise',methods=['POST'])
def visualise():
	tag = request.form['value_tweet']
	tag=re.sub(r'[^\x00-\x7F]+','',tag) 
        location = file_read(tag)
        tweet = file_read_tweet(tag)
        print(location) 
	#print(tweet)
        lat = []
        lng = []
	tweet_l = []
	ctr = 0
        for i in location: 
		if(i != ""): 
        		URL = "http://maps.googleapis.com/maps/api/geocode/json?"
        		addr_key="address"
        		addr_value=re.sub(" ","+",i)
        		sensor_key_val="sensor=false"
        		URL = URL + addr_key + "=" + addr_value + "&" + sensor_key_val
        		googleResponse = urllib.urlopen(URL)
        		jsonResponse = json.loads(googleResponse.read())
        #pprint.pprint(jsonResponse)
        		#pprint.pprint(jsonResponse['results'][0]["geometry"]["location"])
                	lat.append(jsonResponse['results'][0]["geometry"]["location"]['lat'])
			lng.append(jsonResponse['results'][0]["geometry"]["location"]['lng'])
			tweet_l.append(tweet[ctr])
			ctr = ctr + 1
		
	l =[]
	print(len(lat))
	print(len(lng))
	for i in range(len(lat)):
		l.append((lat[i],lng[i],tweet_l[i],tag))		
        #geocode = jsonResponse['results'][0]["geometry"]["location"]['lat'] , jsonResponse['results'][0]["geometry"]["location"]['lng']
	print(l)
	return render_template('map.html',l=l)

@app.route('/map')
def map():
    list_files = listdir("textfiles")
    print(list_files)    
    #list_files = make_response(json.dumps(list_files))
    #list_files = ["CHESUN.txt","Borini.txt"]
    print(list_files) 
    return render_template('list_disp.html',list_f=list_files)


if __name__ == '__main__':
    app.run()
