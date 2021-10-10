import os
import pytesseract
import requests
from PIL import Image
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import MessageEmpty
from pyromod import listen

# pytesseract.pytesseract.tesseract_cmd = r""


BOT_TOKEN = os.environ.get("BOT_TOKEN")
API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")

Bot = Client(
    "OCRBot",
    bot_token = BOT_TOKEN,
    api_id = API_ID,
    api_hash = API_HASH
)

START_TXT = """
Hi {}
I am OCR Bot.

> `I can extract any text from images. All languages supported.`

Send an image to get started.
"""

START_BTN = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Contact', url='https://telegram.dog/strangelets'),
        ]]
    )


@Bot.on_message(filters.command(["start"]))
async def start(bot, update):
    text = START_TXT.format(update.from_user.mention)
    reply_markup = START_BTN
    await update.reply_text(
        text=text,
        disable_web_page_preview=True,
        reply_markup=reply_markup
    )


@Bot.on_message(filters.private & filters.photo)
async def ocr(bot, msg):
    lang_code = hin
    data_url = f"https://github.com/tesseract-ocr/tessdata/raw/main/{lang_code.text}.traineddata"
    dirs = '/app/vendor/tessdata/'
    path = f'{dirs}{lang_code.text}.traineddata'
    if not os.path.exists(path):
        data = requests.get(data_url, allow_redirects=True, headers={'User-Agent': 'Mozilla/5.0'})
        if data.status_code == 200:
            open(path, 'wb').write(data.content)
        else:
            return await msg.reply("`Either the lang code is wrong or the lang is not supported.`", parse_mode='md')
    message = await msg.reply("`Downloading and Extracting...`", parse_mode='md')
    image = await msg.download(file_name=f"text_{msg.from_user.id}.jpg")
    img = Image.open(image)
    text = pytesseract.image_to_string(img, lang=f"{lang_code.text}")
    try:
        await msg.reply(text[:-1], quote=True, disable_web_page_preview=True)
    except MessageEmpty:
        return await msg.reply("`Either the image has no text or the text is not recognizable.`", quote=True, parse_mode='md')
    await message.delete()
    os.remove(image)


    
Bot.run()
