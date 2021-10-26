import os
import random
import tweepy as tw
import pandas as pd
import timeit
from dotenv import load_dotenv
load_dotenv()

consumer_key= os.getenv("consumer_key")
consumer_secret= os.getenv("consumer_secret")
access_token= os.getenv('access_token')
access_token_secret= os.getenv('access_token_secret')


auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)


def search_tweet(q):
    tweet_objects = api.search_tweets(q = q, result_type="mixed", count=100,lang="en")
    
    text = [tweet.text for tweet in tweet_objects]
    dates = [tweet.created_at for tweet in tweet_objects]
    retweet_count = [tweet.retweet_count for tweet in tweet_objects]
    favorite_count = [tweet.favorite_count for tweet in tweet_objects]
    id = [tweet.id_str for tweet in tweet_objects]
    df = pd.DataFrame()
    df['date'] = dates
    df['date'] = pd.to_datetime(df['date'], format="%Y-%m-%d %H:%M:%S")    
    df['text'] = text
    df['retweet_count'] = retweet_count
    df['like'] = favorite_count  
    df['date'] = df['date'].apply(str)
    df["id"] = id
    
    return df


tags = pd.read_csv("tags.csv",sep=",")


list_hashtags = []
list_hashtags = list(tags.columns)
random.shuffle(list_hashtags)
start = timeit.default_timer()
diff = 0
while (diff < 10000000):
    for category in list_hashtags:
        try:
            os.mkdir("twitter_data/"+category+'/')
        except FileExistsError as exc:
            print(exc)    
        hast = tags[category]
        print(hast)        
        for item in hast:
            tweet = []
            ttt = search_tweet(item)
            print("ttt")
            for twit in ttt.text:
                twit = twit.replace("\n","")
                tweet.append(twit)
            
            print(len(tweet))
            name = item + '.csv'
            with open(("twitter_data/"+category+'/'+name), 'a') as filehandle:
                for listitem in tweet:
                    listitem = listitem.replace(",","")
                    if 'RT' not in listitem:
                        if item in listitem:
                            filehandle.write('%s \n' % (listitem))  
            
    stop = timeit.default_timer()
    diff = stop - start
    print(diff)
            

