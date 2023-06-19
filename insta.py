import logging
from pyrogram import Client, idle
from pyrogram.errors import ApiIdInvalid, ApiIdPublishedFlood, AccessTokenInvalid

import Config


logging.basicConfig(
    level=logging.WARNING, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


app = Client(
    ":memory:",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    plugins=dict(root="Instaloader"),
)


# Run Bot
if __name__ == "__main__":
    try:
        app.start()
        uname = app.get_me().username
        print(f"@{uname} Started Successfully!")
        idle()
    except (ApiIdInvalid, ApiIdPublishedFlood):
        raise Exception("Your API_ID/API_HASH is not valid.")
    except AccessTokenInvalid:
        raise Exception("Your BOT_TOKEN is not valid.")
    finally:
        app.stop()
        print("Bot stopped. Alvida!")
