from flask import Flask,make_response
from flask import render_template,request,url_for
import urllib,json
import pprint
import re
import os
app = Flask(__name__)

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
def index():
    list_files = os.listdir("textfiles")
    print(list_files)    
    #list_files = make_response(json.dumps(list_files))
    #list_files = ["CHESUN.txt","Borini.txt"]
    print(list_files) 
    return render_template('list_disp.html',list_f=list_files)

@app.route('/hello/',methods=['POST'])
def hello():
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
        		pprint.pprint(jsonResponse['results'][0]["geometry"]["location"])
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

	

if __name__ == '__main__':
    app.run()
	        
	


