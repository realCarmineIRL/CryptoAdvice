import tweepy as tw
import search_words as sw
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
                       lang=lang).items(num_tweets)
    tweets = [tweet.text for tweet in tweets]
    return tweets


tw_auth = get_twitter_auth(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

print(get_tweets(tw_auth, sw.get_words(), 10))
