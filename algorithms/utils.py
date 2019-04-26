import preprocessor as p
import re
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import string
import pandas as pd

df = None


def preprocess(tweet):
    if tweet.language != 'English':
        return

    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(tweet)
    # after tweepy preprocessing the colon symbol left remain after
    # removing mentions
    tweet = re.sub(r':', '', tweet)
    tweet = re.sub(r'‚Ä¶', '', tweet)
    # replace consecutive non-ASCII characters with a space
    tweet = re.sub(r'[^\x00-\x7F]+', ' ', tweet)
    # remove emojis from tweet
    # tweet = emoji_pattern.sub(r'', tweet)
    # filter using NLTK library append it to a string
    filtered_tokens = [w for w in word_tokens if not w in stop_words and not w in string.punctuation]
    # and w not in emoticons
    return filtered_tokens


def get_tweet_data():
    global df
    if df is None:
        df = pd.read_csv(
            "../data/russian-troll-tweets-master/IRAhandle_tweets_1.csv")
    return df.itertuples()
