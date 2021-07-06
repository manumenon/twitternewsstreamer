from tweepy import API as TwitterApi, OAuthHandler


def gen_auth(consumer_key, consumer_secret, access_token, access_token_secret):
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return auth


class TwitterCrawler:
    def __init__(self, auth, screen_name):
        self.auth = auth
        self.last_since_id = None
        self.screen_name = screen_name
        self.twitter_api = TwitterApi(auth)

    def get_tweet(self):
        if self.last_since_id is None:
            latest_tweets = self.twitter_api.user_timeline(screen_name=self.screen_name, count=1)
        else:
            latest_tweets = self.twitter_api.user_timeline(screen_name=self.screen_name, since_id=self.last_since_id)
        return latest_tweets

    def process_tweets(self, tweets):
        result = []
        for tweet in tweets:
            tweet_dict = dict()
            tweet_dict['tweet_text'] = tweet.text
            tweet_dict['tweet_id'] = tweet.id
            tweet_dict['created_at'] = tweet.created_at.strftime("%Y-%m-%d %H:%M:%S %Z")
            tweet_dict["tweet_by"] = tweet.user.screen_name
            self.last_since_id = tweet.id
            result.append(tweet_dict)
        return result

    def pull_latest_tweets(self):
        tweets = self.get_tweet()
        return self.process_tweets(tweets)
