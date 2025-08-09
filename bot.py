# Don't Remove Credit @RajGor_Paras
# For Support Join @CineHub_Cinema
#
# Copyright (C) 2025 by RajGor_Paras@Github, < https://github.com/RajGor-Paras >.
#
# This file is part of < https://github.com/RajGor-Paras/FileStore > project,
# and is released under the MIT License.
# Please see < https://github.com/RajGor-Paras/FileStore/blob/master/LICENSE >
#
# All rights reserved.

from aiohttp import web
from plugins import web_server
import asyncio
import pyromod.listen
from pyrogram import Client
from pyrogram.enums import ParseMode
import sys
import pytz
from datetime import datetime
#RajGor_Paras on Tg
from config import *
from database.db_premium import *
from database.database import *
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import logging

# Suppress APScheduler logs below WARNING level
logging.getLogger("apscheduler").setLevel(logging.WARNING)

scheduler = AsyncIOScheduler(timezone="Asia/Kolkata")
scheduler.add_job(remove_expired_users, "interval", seconds=10)

# Reset verify count for all users daily at 00:00 IST
async def daily_reset_task():
    try:
        await db.reset_all_verify_counts()
    except Exception:
        pass  

scheduler.add_job(daily_reset_task, "cron", hour=0, minute=0)
#scheduler.start()


name ="""
 BY CODEFLIX BOTS
"""

def get_indian_time():
    """Returns the current time in IST."""
    ist = pytz.timezone("Asia/Kolkata")
    return datetime.now(ist)

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="Bot",
            api_hash=API_HASH,
            api_id=APP_ID,
            plugins={
                "root": "plugins"
            },
            workers=TG_BOT_WORKERS,
            bot_token=TG_BOT_TOKEN
        )
        self.LOGGER = LOGGER
        self.db_channel = None  # Will be set in start()

    async def start(self):
        # First, start the client
        await super().start()
        
        # Get bot info
        me = await self.get_me()
        print(f"Bot started: {me.first_name}")
        
        # Initialize db_channel
        try:
            self.db_channel = await self.get_chat(CHANNEL_ID)
            print(f"Database channel set to: {self.db_channel.title} (ID: {self.db_channel.id})")
        except Exception as e:
            print(f"Failed to initialize database channel: {e}")
            print("Please make sure the bot is an admin in the channel and CHANNEL_ID is set correctly")
            raise
        
        # Send restart notification after client is fully initialized
        try:
            await self.send_message(
                chat_id=OWNER_ID,
                text="Bot restarted by @RajGor_Paras"
            )
        except Exception as e:
            print(f"Failed to send restart notification: {e}")
        
        return self

    async def stop(self, *args):
        await super().stop()
        print("Bot stopped.")

    def run(self):
        """Run the bot."""
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.start())
        print("Bot is now running. Thanks to @RajGor_Paras")
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            print("Shutting down...")
        finally:
            loop.run_until_complete(self.stop())

#
# Copyright (C) 2025 by Codeflix-Bots@Github, < https://github.com/Codeflix-Bots >.
#
# This file is part of < https://github.com/Codeflix-Bots/FileStore > project,
# and is released under the MIT License.
# Please see < https://github.com/Codeflix-Bots/FileStore/blob/master/LICENSE >
#
# All rights reserved.