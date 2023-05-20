from pyTelegramBotAPI import telebot
from pytube import YouTube

bot = telebot.TeleBot(token="6236996276:AAGtndPgpHa6c9wXy8hzXSqVoPBr0Wkjtbw")


@bot.message_handler(commands=["start", "help"])

def youtube_download(message):
    yt = YouTube(message)
    file = yt.streams.first().download()
    
@bot.message_handler(func=lambda message: True)
def echo_call(message):
    bot.reply_to(message, text=message.text)


bot.infinity_polling()
