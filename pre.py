import pandas as pd
import re
import nltk
from collections import OrderedDict
from nltk.corpus import stopwords
from collections import Counter
from urllib.parse import urlparse
from nltk.corpus import stopwords
import numpy as np
from nltk.stem import WordNetLemmatizer
import glob
import os
from nltk.corpus import wordnet
lemmatizer = WordNetLemmatizer()

def get_wordnet_pos(word):
    """Map POS tag to first character lemmatize() accepts"""
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}

    return tag_dict.get(tag, wordnet.NOUN)



STOPWORDS = set(stopwords.words('english'))


def remove_emoji(string):
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)


def remove_stopwords(text):
    return " ".join([word for word in str(text).split() if word not in STOPWORDS])



my_list = os.listdir('twitter_data')
folder_path = "twitter_data/"
for item in my_list:
    if item == ".DS_Store":
        my_list.remove(item)
for filename in my_list:
    folder_name = folder_path + filename +"/"
    try:
        os.mkdir("clean_twitter_data/"+filename+'/')
    except FileExistsError as exc:
        print(exc)    

    print(folder_name)
    for hast in glob.glob(os.path.join(folder_name,'*.csv')):
        print(hast)
        try:
            df = pd.read_csv(hast, sep=',',header=None) 
            hast = os.path.basename(hast)
            hast = hast.replace(".csv","")

            print(df.columns)
            df[0] = df[0].apply(str)
            df[0]  = df[0].str.lower()
            df = df.drop_duplicates(subset=[0])

            df[0] = df[0].apply(lambda x: re.split('https:\/\/.*', str(x))[0])
            df[0] = df[0].apply(lambda x: re.split('http:\/\/.*', str(x))[0])
            df[0] = df[0].apply(lambda x: re.split('www:\/\/.*', str(x))[0])
            df[0] = df[0].apply(lambda x: re.split('html:\/\/.*', str(x))[0])
            df[0] = df[0].str.replace(r'\S*twitter.com\S*', '')





            df[0] = df[0].apply(remove_stopwords)
            df[0] = df[0].apply(remove_emoji)


            df[0] = df[0].str.replace('[^a-zA-Z0-9]', r' ')



            df[0]= df[0].str.replace(r'\s+', ' ')


            df = df[df[0] !='']


            tweet = []
            for i in range(len(df)):
                sentence = df[0].iloc[i]
                tweet.append([lemmatizer.lemmatize(w, get_wordnet_pos(w)) for w in nltk.word_tokenize(sentence)])

            df[0] = tweet


            df.to_csv("clean_twitter_data/"+filename+'/'+hast+'.csv',index=False, sep=',', encoding='utf-8')
        except:
            pass
