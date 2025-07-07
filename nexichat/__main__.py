import sys
import asyncio
import importlib
from flask import Flask
import threading
import config
from pyrogram import idle
from pyrogram.types import BotCommand
from config import OWNER_ID
from nexichat import LOGGER, nexichat, load_clone_owners
from nexichat.modules import ALL_MODULES
from nexichat.modules.Clone import restart_bots


async def anony_boot():
    try:
        await nexichat.start()
        try:
            await nexichat.send_message(int(OWNER_ID), f"**{nexichat.mention} Is started✅**")
        except Exception as ex:
            LOGGER.info(f"@{nexichat.username} Started, please start the bot from owner id.")
    
        asyncio.create_task(restart_bots())
        
        await load_clone_owners()
        
    except Exception as ex:
        LOGGER.error(ex)

    for all_module in ALL_MODULES:
        importlib.import_module("nexichat.modules." + all_module)
        LOGGER.info(f"Successfully imported : {all_module}")

    
    try:
        await nexichat.set_bot_commands(
            commands=[
                BotCommand("start", "Start the bot"),
                BotCommand("help", "Get the help menu"),
                BotCommand("clone", "Make your own chatbot"),
                BotCommand("cloned", "Get List of all cloned bot"),
                BotCommand("ping", "Check if the bot is alive or dead"),
                BotCommand("id", "Get users user_id"),
                BotCommand("stats", "Check bot stats"),
                BotCommand("gcast", "Broadcast any message to groups/users"),
                
            ]
        )
        LOGGER.info("Bot commands set successfully.")
    except Exception as ex:
        LOGGER.error(f"Failed to set bot commands: {ex}")
    
    LOGGER.info(f"@{nexichat.username} Started.")
    
    await idle()


app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is running"

def run_flask():
    app.run(host="0.0.0.0", port=8000)

if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
    asyncio.get_event_loop().run_until_complete(anony_boot())
    LOGGER.info("Stopping nexichat Bot...")
