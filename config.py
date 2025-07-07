from os import getenv

from dotenv import load_dotenv

load_dotenv()

API_ID = "14050586"
# -------------------------------------------------------------
API_HASH = "42a60d9c657b106370c79bb0a8ac560c"
# --------------------------------------------------------------
BOT_TOKEN = getenv("BOT_TOKEN", None)
MONGO_URL = getenv("MONGO_URL", None)
OWNER_ID = int(getenv("OWNER_ID", "6068463116"))
SUPPORT_GRP = "synaxchatgroup"
UPDATE_CHNL = "synaxnetwork"
OWNER_USERNAME = "coder_s4nax"
    
