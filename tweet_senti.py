import sys
import MySQLdb
from textblob import TextBlob
import re
import matplotlib.pyplot as plt
import seaborn

def clean_tweets(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

def fetch(tags):
    try:
        lang = []
        negative = []
        positive = []
        neutral = []
        for a in tags:
            pos = 0
            neg = 0
            neu = 0
            tot = 0
            conn = MySQLdb.connect("localhost","root","","ANAL")
            c = conn.cursor()
            c.execute("SELECT tweet FROM tweets WHERE tweet LIKE %s" , ("% "+a+" %",))
            for row in c:
                test = get_sentiment(row[0])
                if(test > 0):
                    pos = pos+1
                elif(test == 0):
                    neu = neu+1
                else:
                    neg = neg+1
                tot = tot+1
            print "For "+a+": "
            print "Positive tweets :"+format(100*pos/tot)+"%"
            print "Neutral tweets :"+format(100*neu/tot)+"%"
            print "Negative tweets :"+format(100*neg/tot)+"%"
            print "\r"
            lang.append(a)
            negative.append(100*neg/tot)
            positive.append(100*pos/tot)
            c.close()
        # plt.hist([positive[0], positive[1], positive[2]], label=[lang[0], lang[1], lang[2]])
        # plt.legend()
        # plt.title("")
        # plt.xlabel("")
        # plt.ylabel("")
        # plt.show()
    except:
        print "SQL Error"
    finally:
        pass
    return 0

def get_sentiment(text):
    analysis = TextBlob(clean_tweets(text))
    return analysis.sentiment.polarity

q = sys.argv[1:]
q_len = len(q)
fetch(q)
