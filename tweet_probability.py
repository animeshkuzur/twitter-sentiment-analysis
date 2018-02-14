import sklearn
from sklearn import datasets
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import numpy as np
from sklearn import metrics
from sklearn.linear_model import SGDClassifier
import sys
import MySQLdb
import re
# In[25]:

def clean_tweets(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

q = sys.argv[1:]
q_len = len(q)
categories = q
#categories = ['python', 'java', 'php', 'javascript']

tweets = []
# target is classification of tweets based on index of categories
target = []
tar = 0
for tag in q:
	conn = MySQLdb.connect("localhost","root","","ANAL")
	c = conn.cursor()
	c.execute("SELECT tweet FROM tweets WHERE tweet LIKE %s" , ("% "+tag+" %",))
	for row in c:
		text = clean_tweets(row[0])
		tweets.append(text)
		target.append(tar)
	c.close()
	tar=tar+1



# In[26]:

tweets_bunch = sklearn.datasets.base.Bunch(data=tweets, target=target, target_names=categories)


# In[27]:


count_vect = CountVectorizer()
tweets_tokenized = count_vect.fit_transform(tweets_bunch.data)
tweets_tokenized.shape


# In[28]:

print (count_vect.vocabulary_.get(u'php'))
print (count_vect.vocabulary_.get(u'programming'))


# In[29]:


tf_transformer = TfidfTransformer(use_idf=False).fit(tweets_tokenized)
tweets_tokenized_tf = tf_transformer.transform(tweets_tokenized)
tweets_tokenized_tf.shape


# In[30]:

tfidf_transformer = TfidfTransformer()
tweets_tokenized_tfidf = tfidf_transformer.fit_transform(tweets_tokenized)
tweets_tokenized.shape


# In[31]:


clf = MultinomialNB().fit(tweets_tokenized_tfidf, tweets_bunch.target)


# In[36]:

tweets_new = []
# target is classification of tweets based on index of categories
targets_new = []
tar = 0
for tag in q:
	conn = MySQLdb.connect("localhost","root","","ANAL")
	c = conn.cursor()
	c.execute("SELECT tweet FROM tweets_test WHERE tweet LIKE %s" , ("% "+tag+" %",))
	for row in c:
		text = clean_tweets(row[0])
		tweets_new.append(text)
		targets_new.append(tar)
	c.close()
	tar=tar+1

#tweets_new = ['Python is awesome', 'Java is popular']
#targets_new = [0, 2]
X_new_counts = count_vect.transform(tweets_new)
X_new_tfidf = tfidf_transformer.transform(X_new_counts)

predicted = clf.predict(X_new_tfidf)

for tweet, category in zip(tweets_new, predicted):
    print('%r => %s' % (tweet, tweets_bunch.target_names[category]))


# In[37]:


text_clf = Pipeline([('vect', CountVectorizer()), ('tfidf', TfidfTransformer()), ('clf', MultinomialNB()),])


# In[38]:

text_clf = text_clf.fit(tweets_bunch.data, tweets_bunch.target)


# In[39]:


tweets_bunch_test = sklearn.datasets.base.Bunch(data=tweets_new, categories=categories, target=targets_new)
tweets_test = tweets_bunch_test.data
predicted = text_clf.predict(tweets_test)
print format(np.mean(predicted == tweets_bunch_test.target)) + " is the probability of prediction from BAYES"


# In[41]:


print(metrics.classification_report(tweets_bunch_test.target, predicted, target_names=tweets_bunch_test.categories))


# In[42]:


text_clf = Pipeline([('vect', CountVectorizer()),
('tfidf', TfidfTransformer()),
('clf', SGDClassifier(loss='hinge', penalty='l2',
alpha=1e-3, n_iter=5, random_state=42)),
])
_ = text_clf.fit(tweets_bunch_test.data, tweets_bunch_test.target)
predicted = text_clf.predict(tweets_test)
for tweet, category in zip(tweets_new, predicted):
    print('%r => %s' % (tweet, tweets_bunch.target_names[category]))
print format(np.mean(predicted == tweets_bunch_test.target)) + " is the probability of prediction from SVM"


# In[43]:


print(metrics.classification_report(tweets_bunch_test.target, predicted, target_names=tweets_bunch_test.categories))