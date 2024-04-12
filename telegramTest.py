# pip install python-telegram-bot

import telegram
import asyncio

bot = telegram.Bot(token="6942953027:AAFIise7PasqSNx9JiQVWjv71QmxmtjY5qU")
chat_id = "7073835255"

asyncio.run(bot.sendMessage(chat_id=chat_id, text="test working fine"))