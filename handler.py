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

PG_USER = os.environ.get('PG_USER')
PG_PASS = os.environ.get('PG_PASS')
PG_HOST = os.environ.get('PG_HOST')
PG_PORT = os.environ.get('PG_PORT')
PG_DB = os.environ.get('PG_DB')

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
    connection = psycopg2.connect(user = PG_USER,
                                  password = PG_PASS,
                                  host = PG_HOST,
                                  port = PG_PORT,
                                  database = PG_DB)
    cursor = connection.cursor()
    upd = f'UPDATE sentiments SET score = {polarity * 100} where id = 1'
    cursor.execute(upd)
    connection.commit()
    cursor.close()
    connection.close()