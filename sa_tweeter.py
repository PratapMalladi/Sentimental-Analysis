# -*- coding: utf-8 -*-
"""
@author:Pratap
"""

import re
import tweepy #https://github.com/tweepy/tweepy
from wordcloud import WordCloud

#Twitter API credentials

consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""


def get_all_tweets(screen_name):
    auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    alltweets = []	
    new_tweets = api.user_timeline(screen_name = screen_name,count=200)
    alltweets.extend(new_tweets)
    
    oldest = alltweets[-1].id - 1
    while len(new_tweets)>0:
        new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
        #save most recent tweets
        alltweets.extend(new_tweets)
        #update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1
        print ("...%s tweets downloaded so far" % (len(alltweets)))                # tweet.get('user', {}).get('location', {})
 
    outtweets = [[tweet.created_at,tweet.entities["hashtags"],tweet.entities["user_mentions"],tweet.favorite_count,
                  tweet.geo,tweet.id_str,tweet.lang,tweet.place,tweet.retweet_count,tweet.retweeted,tweet.source,tweet.text,
                  tweet._json["user"]["location"],tweet._json["user"]["name"],tweet._json["user"]["time_zone"],
                  tweet._json["user"]["utc_offset"]] for tweet in alltweets]
    
    import pandas as pd
    tweets_df = pd.DataFrame(columns = ["time","hashtags","user_mentions","favorite_count",
                                    "geo","id_str","lang","place","retweet_count","retweeted","source",
                                    "text","location","name","time_zone","utc_offset"])
    tweets_df["time"]  = pd.Series([str(i[0]) for i in outtweets])
    tweets_df["hashtags"] = pd.Series([str(i[1]) for i in outtweets])
    tweets_df["user_mentions"] = pd.Series([str(i[2]) for i in outtweets])
    tweets_df["favorite_count"] = pd.Series([str(i[3]) for i in outtweets])
    tweets_df["geo"] = pd.Series([str(i[4]) for i in outtweets])
    tweets_df["id_str"] = pd.Series([str(i[5]) for i in outtweets])
    tweets_df["lang"] = pd.Series([str(i[6]) for i in outtweets])
    tweets_df["place"] = pd.Series([str(i[7]) for i in outtweets])
    tweets_df["retweet_count"] = pd.Series([str(i[8]) for i in outtweets])
    tweets_df["retweeted"] = pd.Series([str(i[9]) for i in outtweets])
    tweets_df["source"] = pd.Series([str(i[10]) for i in outtweets])
    tweets_df["text"] = pd.Series([str(i[11]) for i in outtweets])
    tweets_df["location"] = pd.Series([str(i[12]) for i in outtweets])
    tweets_df["name"] = pd.Series([str(i[13]) for i in outtweets])
    tweets_df["time_zone"] = pd.Series([str(i[14]) for i in outtweets])
    tweets_df["utc_offset"] = pd.Series([str(i[15]) for i in outtweets])
    tweets_df.to_csv(screen_name+"_tweets.csv")
    return tweets_df
import os 
os.getcwd()
microsoft = get_all_tweets("Microsoft")

		
text=microsoft.text
#converted the list into paragragh
ip_rev_string = " ".join(text)
#implementing with preprocessing techniques
ip_rev_string = re.sub("[^A-Za-z" "]+"," ",ip_rev_string).lower()
ip_rev_string = re.sub("[0-9" "]+"," ",ip_rev_string)

ip_reviews_words = ip_rev_string.split(" ")

#stop words
from nltk.corpus import stopwords
stop_words = stopwords.words('english')
stopwordss=[w for w in ip_reviews_words if not w in stop_words]
    

#we are using stopwordscommand to remove the stopwords in reviews
from nltk.stem import PorterStemmer
ps=PorterStemmer()
stemm=[]
for w in stopwordss:
    stemm.append(ps.stem(w))
    
# Joinining all the reviews into single paragraph 
ip_rev_string = " ".join(stemm)


wordcloud_ip = WordCloud(
                      background_color='white',
                      width=1800,
                      height=1400
                     ).generate(ip_rev_string)

import matplotlib.pyplot as plt
plt.imshow(wordcloud_ip)

#creating positive words
with open("C:/Users/Sunitha/Desktop/Ecil_Awareness_Session/UseC/positive-stopwords.txt","r") as pos:
  poswords = pos.read().split("\n")

posword=poswords[0:]

with open("C:/Users/Sunitha/Desktop/Ecil_Awareness_Session/UseC/negative-stopwords.txt","r") as neg:
  negwords = neg.read().split("\n")

negwords = negwords[1:]

# negative word cloud
# Choosing the only words which are present in negwords
ip_neg_in_neg = " ".join ([w for w in ip_reviews_words if w in negwords])

wordcloud_neg_in_neg = WordCloud(
                      background_color='black',
                      width=1800,
                      height=1400
                     ).generate(ip_neg_in_neg)

plt.imshow(wordcloud_neg_in_neg)

# Positive word cloud
# Choosing the only words which are present in positive words
ip_pos_in_pos = " ".join ([w for w in ip_reviews_words if w in poswords])
wordcloud_pos_in_pos = WordCloud(
                      background_color='white',
                      width=1800,
                      height=1400
                     ).generate(ip_pos_in_pos)

plt.imshow(wordcloud_pos_in_pos)

from textblob import TextBlob
#text = open("trimmer.txt")
#text=text.read()
text=microsoft.text

ip_pos_in_pos
blob=TextBlob(ip_neg_in_neg)
print(blob.sentiment) 

