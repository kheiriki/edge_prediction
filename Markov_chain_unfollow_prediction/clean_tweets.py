import glob

import preprocessor as p
p.set_options(p.OPT.URL,p.OPT.MENTION,p.OPT.HASHTAG,p.OPT.RESERVED,p.OPT.EMOJI,p.OPT.SMILEY,p.OPT.NUMBER)
import pandas as np
import string
import re
import nltk
nltk.download('stopwords')
stopwords = nltk.corpus.stopwords.words('english')
from nltk.stem import WordNetLemmatizer
wordnet_lemmatizer = WordNetLemmatizer()
nltk.download('wordnet')
import numpy as np
from tqdm import tqdm
import os
import pickle

from stop_words import get_stop_words
from nltk.corpus import stopwords


thestopwords =list(get_stop_words('en'))         #About 900 stopwords

nltk_words = list(stopwords.words('english')) #About 150 stopwords
thestopwords.extend(nltk_words)
extra_stop_words=open('extra_stop_words').read().splitlines()
thestopwords.extend(extra_stop_words)


punctuations=[]
punctuations.extend(string.punctuation)
punctuations.extend(["”","“","‘","’"])
punctuations="".join(punctuations)


def remove_URL(text):
    return re.sub(r"http\S+", "", text)

def clean_text(text):
    text=remove_URL(text)
    text=p.clean(text)
    text=text.lower()
    text=re.sub(r"[\"!•#$%&\'()*\+,-./:;<=>?@\[\]\\^_`{|}~”“‘’0123456789]", " ", text)
    #text="".join([i for i in text if i not in punctuations])
    text=text.split(' ')
    text=[t for t in text if t !=' ' and len(t)>=2]

    text_stop_words_removed= [t for t in text if t not in thestopwords]
    text_stop_words_removed = [wordnet_lemmatizer.lemmatize(word) for word in text_stop_words_removed]
    text_with_stop_words=[wordnet_lemmatizer.lemmatize(word) for word in text]
    return " ".join(text_stop_words_removed)," ".join(text_with_stop_words)

rounds=["round"+str(i) for i in range(1,16)]

clean_text('http://t.co/Dkv3DzKHMv...................................')


#for f in ['../round2/Tweets/282366563_Tweet.pkl', '../round2/Tweets/796032002_Tweet.pkl', '../round2/Tweets/14102589_Tweet.pkl', '../round2/Tweets/1717073682_Tweet.pkl']:
    #print(f)
    #tweets=pickle.load(open(f,'rb'))
    #for tweet in tqdm(tweets):
    #   clean_text(str(tweet['text']))

# for r in rounds:
#     os.system("mkdir  ../{}/clean_texts".format(r))

for r in tqdm(rounds[0:1]):
    print(r)
    files=glob.glob("../{}/Tweets/*.pkl".format(r))
    for f in tqdm(files):
        tweets=pickle.load(open(f,'rb'))
        tweets=tweets[0]
        
        fp=open("../{}/clean_texts/{}.csv".format(r,f.split('/')[-1].split('_')[0]),'w')
        for tweet in tweets:
            t1,t2=clean_text(str(tweet['text']))
            fp.write("{},{},{}\n".format(tweet['id'],t1,t2))
            #print(tweet['id'],tweet['text'],t1,t2)
        fp.close()
    1/0
