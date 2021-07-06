from telethon import TelegramClient, events, sync


class TelegramHandler:

    def __init__(self,creds):
        api_id = creds['telegram_api_id']
        api_hash = creds['telegram_api_hash']
        username = creds['telegram_username']
        self.client = TelegramClient(username, api_id, api_hash)
        self.client.start()
        self.channel_id = int(creds['telegram_channel_id'])

    async def sent_message(self,message):
        await self.client.send_message(self.channel_id, message)