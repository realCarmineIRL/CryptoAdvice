import tweepy as tw
import search_words as sw

CONSUMER_KEY = 'nb20uNetSa2NbW5q4tcZ4R7jC'
CONSUMER_SECRET = '7Cv1YiAQ8UywFlnV3yPPWtqGdcO0YhGCbFj4hGEbjZtN5MwUYS'
ACCESS_TOKEN = '52314137-BFN0TuBACsP0klUof7E2Gnkll1ouYZQ7PIULTlIiZ'
ACCESS_TOKEN_SECRET = 'PjJqIuMHDv223716kMR3d5wJ3J8aHh6ysjYdt97n7K7Bi'


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
