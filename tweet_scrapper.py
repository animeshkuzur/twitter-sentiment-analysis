import sys
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import MySQLdb
import json
from textblob import TextBlob
import re
import seaborn

access_token = ""
access_token_secret = ""
consumer_key = ""
consumer_secret = ""

class listeners(StreamListener):

    def on_data(self, data):
        all_data = json.loads(data)
        try:
            if all_data['place']['country']:
                conn = MySQLdb.connect("localhost","root","","ANAL")
                c = conn.cursor()
                c.execute("""INSERT INTO tweets (username,tweet,likes,friends,followers,retweets,country) VALUES (%s,%s,%s,%s,%s,%s,%s);""",(all_data['user']['screen_name'],all_data['text'],all_data['user']['favourites_count'],all_data['user']['friends_count'],all_data['user']['followers_count'],all_data['user']['statuses_count'],all_data['place']['country']))
                conn.commit()
                c.close()
            else:
                pass
        except:
            conn = MySQLdb.connect("localhost","root","","ANAL")
            c = conn.cursor()
            c.execute("""INSERT INTO tweets (username,tweet,likes,friends,followers,retweets,country) VALUES (%s,%s,%s,%s,%s,%s,%s);""",(all_data['user']['screen_name'],all_data['text'],all_data['user']['favourites_count'],all_data['user']['friends_count'],all_data['user']['followers_count'],all_data['user']['statuses_count'],"NULL"))
            conn.commit()
            c.close()
            return True
        finally:
            return True
            
    def on_error(self, status):
        print "Unable to fetch tweets..."
        print status


def gettweets(q,q_len):
    l = listeners()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    stream.filter(track=q,languages=['en'])
    return 0

q = sys.argv[1:]
q_len = len(q)
run = gettweets(q,q_len)
