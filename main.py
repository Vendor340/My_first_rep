import pytube

from pyTelegramBotAPI import telebot
from pytube import YouTube

bot = telebot.TeleBot(token="6236996276:AAGtndPgpHa6c9wXy8hzXSqVoPBr0Wkjtbw")


@bot.message_handler(commands=["start", "help"])
def start_bot(message):
    bot.send_message(message.chat.id, text="Enter title of video, which you want to download?")


@bot.message_handler(func=lambda message: True)
def Search_video(message):
    yt = pytube.Search(message)
    for video in yt.results:
        bot.send_message(message.chat.id, text=f"Title: {video.title}, url: {video.watch_url}")

bot.infinity_polling()
