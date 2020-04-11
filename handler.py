try:
  import unzip_requirements
except ImportError:
  pass

import tweepy as tw
from textblob import TextBlob
import logging
import os
import psycopg2


CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


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
    tweet_analysis = [TextBlob(tweet.full_text).sentiment.polarity > 0 for tweet in tweets]
    score = sum(tweet_analysis) / len(tweet_analysis)
    return score

def run(event, context):
    logger.info("starting")
    tw_auth = get_twitter_auth(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    query = get_words()
    polarity = get_tweet_sentiment(get_tweets(tw_auth, query, 200))
    logger.info(polarity)
    connection = psycopg2.connect(user = "ifqhkeevsenmek",
                                  password = "d4379a8cf1896eef9977b943d46b551c890ebb47be25ba1888b67595e84be41b",
                                  host = "ec2-46-137-177-160.eu-west-1.compute.amazonaws.com",
                                  port = "5432",
                                  database = "dapeujevpredau")
    cursor = connection.cursor()
    upd = f'UPDATE sentiments SET score = {polarity * 100} where id = 1'
    cursor.execute(upd)
    connection.commit()
    cursor.close()
    connection.close()