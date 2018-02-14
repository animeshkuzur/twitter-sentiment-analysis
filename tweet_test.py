import sys
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import MySQLdb
import json

access_token = "695361221625716736-5Yr0FX65HgVJ3fyfLY9r1QaVfmfZJZT"
access_token_secret = "9NpLRpXXagTR3AkuYk4Q5FZ4r0YqvdruMUxJVbGwZV8tn"
consumer_key = "oHplxBuIDaYlVhYNEOSVDb3mc"
consumer_secret = "lAL13lMy3rQy66GOfy4Ln3DNlmXljkdzKX7X7FtnxTA8yDZpg4"

class listeners(StreamListener):

    def on_data(self, data):
        all_data = json.loads(data)
        try:
            if all_data['place']['country']:
                conn = MySQLdb.connect("localhost","root","","ANAL")
                c = conn.cursor()
                c.execute("""INSERT INTO tweets_test (username,tweet,likes,friends,followers,retweets,country) VALUES (%s,%s,%s,%s,%s,%s,%s);""",(all_data['user']['screen_name'],all_data['text'],all_data['user']['favourites_count'],all_data['user']['friends_count'],all_data['user']['followers_count'],all_data['user']['statuses_count'],all_data['place']['country']))
                conn.commit()
                c.close()
            else:
                pass
        except:
            conn = MySQLdb.connect("localhost","root","","ANAL")
            c = conn.cursor()
            c.execute("""INSERT INTO tweets_test (username,tweet,likes,friends,followers,retweets,country) VALUES (%s,%s,%s,%s,%s,%s,%s);""",(all_data['user']['screen_name'],all_data['text'],all_data['user']['favourites_count'],all_data['user']['friends_count'],all_data['user']['followers_count'],all_data['user']['statuses_count'],"NULL"))
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