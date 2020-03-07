import tweepy as tw
import search_words as sw
from textblob import TextBlob
import os

CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')


def get_twitter_auth(consumer_key, consumer_secret, access_token, access_token_secret):
    auth = tw.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    return auth


def get_tweets(auth, search_words, num_tweets, lang="en"):
    api = tw.API(auth, wait_on_rate_limit=True)
    tweets = tw.Cursor(api.search,
                       q=search_words,
                       lang=lang,
                       tweet_mode="extended").items(num_tweets)
    return tweets


def get_tweet_sentiment(tweets):
    tweet_analysis = [[tweet.full_text, tweet.created_at, TextBlob(tweet.full_text).sentiment] for tweet in tweets]
    return tweet_analysis


tw_auth = get_twitter_auth(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

query = sw.get_words()

print(get_tweet_sentiment(get_tweets(tw_auth, query, 1)))
