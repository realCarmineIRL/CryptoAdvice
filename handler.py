try:
  import unzip_requirements
except ImportError:
  pass

import tweepy as tw
from textblob import TextBlob
import os
import numpy as np
import logging
from datetime import datetime
import boto3

CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

s3 = boto3.client("s3")
bucket_resource = s3

def get_twitter_auth(consumer_key, consumer_secret, access_token, access_token_secret):
    auth = tw.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    return auth

def get_words():
    words = "bitcoin -filter:retweets"
    return words


def get_tweets(auth, search_words, num_tweets, lang="en"):
    logger.info("Getting twitter data")
    api = tw.API(auth, wait_on_rate_limit=True)
    tweets = tw.Cursor(api.search,
                       q=search_words,
                       lang=lang,
                       tweet_mode="extended").items(num_tweets)
    return tweets


def get_tweet_sentiment(tweets):
    logger.info("creating csv")
    tweet_analysis = [[tweet.full_text.replace('"','').replace('\n',''), tweet.created_at, TextBlob(tweet.full_text).sentiment.polarity, TextBlob(tweet.full_text).sentiment.subjectivity] for tweet in tweets]
    return tweet_analysis

def run(event, context):
    logger.info("Creating CSV")
    date = datetime.today().strftime('%Y%m%d%H%M')
    file_name = "tweets_{}.csv".format(date)
    filepath = '/tmp/'
    key = "year={}/month={}/day={}/{}".format(date[0:4], date[4:6], date[6:8], file_name)
    tw_auth = get_twitter_auth(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    query = get_words()
    header = 'tweet, time, polarity, subjetivity'
    tweets = get_tweet_sentiment(get_tweets(tw_auth, query, 200))
    np.savetxt(filepath + file_name, tweets, delimiter=",", fmt='"%s"', header=header)
    logger.info("Uploading to S3")
    bucket_resource.upload_file(
        Bucket='crypto-advice-tweets',
        Filename= filepath + file_name,
        Key=key
    )
