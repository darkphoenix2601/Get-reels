import os
import re
import asyncio
import shutil
from Config import INSTA_USERNAME, INSTA_PASSWORD
from pyrogram import Client, filters
from .database.users_sql import get_info


@Client.on_message(filters.private & ~filters.regex(r'^/'))
async def main(_, msg):
    if 'instagram.com' not in msg.text:
        return
    status = await msg.reply('Please Wait...', quote=True)
    pattern = re.compile(r'^(https?:[/][/])?(www\.)?instagram.com[/](p|reel)[/]([A-Za-z0-9-_]+)')
    try:
        matches = pattern.search(msg.text)
        post_id = matches.group(4)
        username, password = await get_info(msg.from_user.id)
        if not username:
            username = INSTA_USERNAME
            password = INSTA_PASSWORD
        if username and password:
            command = f"instaloader --no-metadata-json -l {username} -p {password} -- -{post_id}"
        else:
            command = f"instaloader --no-metadata-json -- -{post_id}"
        proc = await asyncio.subprocess.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await proc.communicate()
        if "wrong password" in str(stderr).lower():
            raise Exception('Wrong Instagram Password.')
        path = f"-{post_id}"
        photos, videos, caption = post_prep(path)
        if not photos and not videos:
            await status.delete()
            await msg.reply("No Such Instagram Post Exists.")
            return
        if len(photos+videos) == 1:
            if caption:
                caption += "\n\nBy @Professer_Ashu"
            else:
                caption = "By @Professer_Ashu"
            if photos:
                for photo in photos:
                    await msg.reply_photo(photo, caption)
            if videos:
                for video in videos:
                    await msg.reply_video(video, caption)
        else:
            if photos:
                for photo in photos:
                    await msg.reply_photo(photo)
            if videos:
                for video in videos:
                    await msg.reply_video(video)
            if caption:
                await msg.reply(f"**POST CAPTION : **\n\n{caption} \n\nBy @Professer_Ashu")
        await status.delete()
        shutil.rmtree(path)
    except AttributeError:
        await status.delete()
        await msg.reply(error)


error = """
Please send me a valid instagram post link.
It must be like one of the given below

**Note** : To get profile picture of a account use "`/profile_pic instagram-username`". Link won't work.
"""


def post_prep(path):
    if not os.path.isdir(path):
        return None, None, None
    files = os.listdir(path)
    photos = []
    videos = []
    caption = ""
    for file in files:
        if file.endswith(".jpg"):
            photos.append(path+'/'+file)
        if file.endswith(".mp4"):
            videos.append(path+'/'+file)
        if file.endswith(".txt"):
            with open(f"{path}/{file}") as f:
                caption = f.read()
    return photos, videos, caption
