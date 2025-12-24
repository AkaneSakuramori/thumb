from pyrogram import Client, filters
from parser import parse_info
from poster import generate_poster
import os

API_ID = 7721764
API_HASH = "a9c08aae19aa4c8b37ff658d1951a1f7"
BOT_TOKEN = "1955186176:AAFa4GFgiUvERzmAp4Jo_E-_q_iT3xBRfM8"

app = Client("posterbot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

os.makedirs("temp", exist_ok=True)

user_data = {}

@app.on_message(filters.private & filters.text)
async def receive_info(client, message):
    user_data[message.from_user.id] = parse_info(message.text)
    await message.reply("🖼️ Now send the background image")

@app.on_message(filters.private & filters.photo)
async def receive_image(client, message):
    uid = message.from_user.id

    if uid not in user_data:
        await message.reply("❌ Send info text first")
        return

    bg_path = await message.download(file_name=f"temp/{uid}_bg.jpg")
    output_path = f"temp/{uid}_poster.png"

    generate_poster(
        bg_path=bg_path,
        data=user_data[uid],
        character_path=None,
        output=output_path
    )

    if not os.path.exists(output_path):
        await message.reply("❌ Poster generation failed")
        return

    await message.reply_photo(photo=open(output_path, "rb"))

    os.remove(bg_path)
    os.remove(output_path)
    del user_data[uid]

app.run()
