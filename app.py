from scripts.orchastrator.twitter_telegram import TwitterTelegramOrc

from scripts.utils.config import config



if __name__ == '__main__':
    import asyncio
    d =TwitterTelegramOrc(config)
    d.add()
    d.scheduler.start()
    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass