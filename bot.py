"""
Sana: 23.02.2022
Dasturchi: Turdibek Jumabaev
Bot: YouTube video va audio yuklovchi
"""

from telebot import TeleBot
from telebot.types import *
import os, config, asyncio
from pytube import *

bot = TeleBot(config.TOKEN)
video = None

def create_keyboard(yt):
    buttons = []
    keyboard = InlineKeyboardMarkup(row_width=1)
    i = 0
    for stream in yt.streams.filter(progressive="True"):
        typ = str(stream).split(" ")[2].split("=")[1][1:-1]
        quality = str(stream).split(" ")[3].split("=")[1][1:-1]

        text_button = "Tip: {}, Sifat: {}".format(typ, quality)
        buttons.append(InlineKeyboardButton(text=text_button, callback_data=str(i)))
        i += 1
    keyboard.add(*buttons)
    return keyboard

@bot.message_handler(commands=["start"])
def start(message):
    text = "Assalom alaykum, men sizga YouTube'dan video yuklab beraman."
    bot.send_message(message.chat.id, text)

@bot.message_handler(content_types=["text"])
def echo(message):
    yt = None
    try:
        yt = YouTube(message.text)
    except:
        bot.send_message(message.chat.id, "Menga YouTube video linkini jo'nating.")
    if yt is not None:
        keyboard = create_keyboard(yt)
        global video
        video = yt
        bot.send_message(message.chat.id, "Yuklab olish uchun formatni tanlang", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda x: True)
def query_hand(call):
    global video 
    bot.send_message(call.from_user.id, "Video yuklanmoqda...")
    video = open(video.streams.filter(progressive='True')[int(call.data)].download(filename="{}".format(call.from_user.id)), "rb")
    bot.send_video(call.from_user.id, video)
    video.close()
    name = f"rm -f {call.from_user.id}"
    os.system(name)
    os.remove("{}.mp4".format(call.from_user.id))

bot.infinity_polling()