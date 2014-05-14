import json
import twitter
#t = twitter.Twitter(domain='api.twitter.com', api_version='1.1')
#print json.dumps(t.trends(), indent=1)
CONSUMER_KEY = 'consumer key'
CONSUMER_SECRET ='consumer secret'
OAUTH_TOKEN = 'oauth token'
OAUTH_TOKEN_SECRET = 'oauth token secret'
count=1400

auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                           CONSUMER_KEY, CONSUMER_SECRET)
def search(q):
        search_results = twitter_api.search.tweets(q=q, count=count)
        statuses = search_results['statuses']
        fn=q+".txt"
        f=open(fn,"w")
#       print("***********************************************")
        f.write(q+"\n")
#       print("***********************************************")
        for i in range(len(statuses)):
                if statuses[i][u'lang']==u'en':
#                       tweet="Tweet "+str(i)+": "+statuses[i][u'text']+"\n"
                        tweet=statuses[i][u'text']+"\n"
                        f.write(tweet.encode('utf-8'))
                        date="Date: "+statuses[i][u'created_at']+"\n"
                        f.write(date)
                        location="Location: "+statuses[i][u'user'][u'location']+"\n"
                        f.write(location.encode('utf-8'))
                        f.write("\n")
twitter_api = twitter.Twitter(auth=auth)
search("#HappyBirthday")
