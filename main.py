import pytube

import telebot

bot = telebot.TeleBot(token="6236996276:AAGtndPgpHa6c9wXy8hzXSqVoPBr0Wkjtbw")


@bot.message_handler(commands=["start", "help"])
def start_bot(message):
    bot.send_message(message.chat.id, text="Enter url of your video")


@bot.message_handler(func=lambda message: message)
def download_video(message):
    yt = pytube.YouTube(message.text)
    stream = yt.streams.first()
    stream.download(filename="video.mp4")
    video = open("video.mp4", "rb")
    bot.send_document(message.chat.id, video.read(), caption=f"{yt.title}.mp4")


bot.infinity_polling()
