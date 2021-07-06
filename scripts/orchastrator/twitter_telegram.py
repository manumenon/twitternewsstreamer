from scripts.message_handlers.telegram_handler import TelegramHandler
from scripts.crawlers.twitter_crawler import TwitterCrawler, gen_auth
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers import SchedulerNotRunningError
from multiprocessing.pool import ThreadPool
from scripts.utils.config import config
from scripts.utils.logging import logger
class TwitterTelegramOrc:

    def __init__(self, config):
        self.config = config

        self.twitter_auth = gen_auth(
            consumer_key=config['twitter_consumer_key'],
            consumer_secret=config['twitter_consumer_secret'],
            access_token=config['twitter_access_token'],
            access_token_secret=config['twitter_access_token_secret']
        )

        self.screen_names = config["twitter_screen_names"]
        self.objs_dict = dict()
        self.telegram = TelegramHandler(config)
        self.scheduler = AsyncIOScheduler()

    def get_tweets(self):
        logger.info("pulling Tweets")
        tweets = []
        for item in self.screen_names:
            if item not in self.objs_dict:
                self.objs_dict[item] = TwitterCrawler(screen_name=item, auth=self.twitter_auth)
                tweets.extend(self.objs_dict[item].pull_latest_tweets())
        return tweets

    async def push_message(self, tweets):
        logger.info("pushing Tweets")
        for tweet in tweets:
            text = "{tweet_by} on {created_at}  tweeted: **{tweet_text} **".format(**tweet)
            await self.telegram.sent_message(text)

    async def  run(self):

        tweets = self.get_tweets()
        await self.push_message(tweets)

    def add(self):
        self.scheduler.add_job(self.run, 'cron', id="slot", second=f'*/{self.config["cron"]}', misfire_grace_time=30)

