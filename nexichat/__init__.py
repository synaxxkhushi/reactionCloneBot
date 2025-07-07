import logging
import time
from pymongo import MongoClient
from Abg import patch
from motor.motor_asyncio import AsyncIOMotorClient as MongoCli
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
import config
import uvloop
import time
SUDOERS = filters.user()
CLONE_OWNERS = {}
uvloop.install()

logging.basicConfig(
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO,
)

logging.getLogger("pyrogram").setLevel(logging.ERROR)
LOGGER = logging.getLogger(__name__)
boot = time.time()
mongodb = MongoCli(config.MONGO_URL)
db = mongodb.Anonymous
mongo = MongoClient(config.MONGO_URL)
mongodb = mongo.VIP
OWNER = config.OWNER_ID
_boot_ = time.time()
clonedb = None
def dbb():
    global db
    global clonedb
    clonedb = {}
    db = {}
    
def sudo():
    global SUDOERS
    OWNER = config.OWNER_ID
    if config.MONGO_URL is None:
        SUDOERS.add(OWNER)
    else:
        sudoersdb = mongodb.sudoers
        sudoers = sudoersdb.find_one({"sudo": "sudo"})
        sudoers = [] if not sudoers else sudoers["sudoers"]
        SUDOERS.add(OWNER)
        if OWNER not in sudoers:
            sudoers.append(OWNER)
            sudoersdb.update_one(
                {"sudo": "sudo"},
                {"$set": {"sudoers": sudoers}},
                upsert=True,
            )
        if sudoers:
            for x in sudoers:
                SUDOERS.add(x)
    print(f"Sudoers Loaded.")

cloneownerdb = db.clone_owners

async def load_clone_owners():
    async for entry in cloneownerdb.find():
        bot_id = entry["bot_id"]
        user_id = entry["user_id"]
        CLONE_OWNERS[bot_id] = user_id

async def save_clonebot_owner(bot_id, user_id):
    await cloneownerdb.update_one(
        {"bot_id": bot_id},
        {"$set": {"user_id": user_id}},
        upsert=True
    )
async def get_clone_owner(bot_id):
    data = await cloneownerdb.find_one({"bot_id": bot_id})
    if data:
        return data["user_id"]
    return None

async def delete_clone_owner(bot_id):
    await cloneownerdb.delete_one({"bot_id": bot_id})
    CLONE_OWNERS.pop(bot_id, None)

async def save_idclonebot_owner(clone_id, user_id):
    await cloneownerdb.update_one(
        {"clone_id": clone_id},
        {"$set": {"user_id": user_id}},
        upsert=True
    )

async def get_idclone_owner(clone_id):
    data = await cloneownerdb.find_one({"clone_id": clone_id})
    if data:
        return data["user_id"]
    return None

    
class nexichat(Client):
    def __init__(self):
        super().__init__(
            name="nexichat",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            in_memory=True,
            parse_mode=ParseMode.DEFAULT,
        )

    async def start(self):
        await super().start()
        self.id = self.me.id
        self.name = self.me.first_name + " " + (self.me.last_name or "")
        self.username = self.me.username
        self.mention = self.me.mention
        
    async def stop(self):
        await super().stop()

def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]
    while count < 4:
        count += 1
        if count < 3:
            remainder, result = divmod(seconds, 60)
        else:
            remainder, result = divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    for i in range(len(time_list)):
        time_list[i] = str(time_list[i]) + time_suffix_list[i]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "
    time_list.reverse()
    ping_time += ":".join(time_list)
    return ping_time
    
sudo()
nexichat = nexichat()
