import pytube
from os import remove
from compress_video import extract_text
from telethon.sync import TelegramClient, events, Button
from config import configure

config = configure()

client = TelegramClient("YoutubeUp", config.API_ID, config.API_HASH)


class User:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.url = None

    def on_progress(self, current, total):
        progress = int((int(current) / int(total)) * 100)
        print(f"uploaded data:{current // 1024} from {total // 1024}")
        print(progress * "#" + f' {progress}%')

    async def download_video(self):
        yt = pytube.YouTube(self.url)

        stream = [i for i in yt.streams.filter(progressive=True).order_by("bitrate")]
        video = stream[len(stream) // 2]
        video.download(filename="video.mp4")
        return video

    async def download_audio(self):
        yt = pytube.YouTube(self.url)
        audio = yt.streams.filter(type="audio").order_by("bitrate")
        audio = audio[len(audio) // 2]
        audio.download(filename=f"{audio.title}.mp3")
        return audio

    @classmethod
    def get_or_create(cls, chat_id):
        users = []
        user = cls(chat_id)
        if chat_id in users:
            return user
        else:
            users.append(chat_id)
            return user


@client.on(events.NewMessage(incoming=True, pattern=r"/start"))
async def get_start(event):
    global user
    chat = await event.get_chat()
    user = User.get_or_create(chat.id)
    keyboard = [Button.inline(text=i, data=i) for i in ["/download_video", "/extract_audio", "/extract_text"]]

    await client.send_message(chat, "Welcome to the Youtube downloader!", buttons=keyboard)


@client.on(events.CallbackQuery(func=lambda f: f))
async def callback_handler(event):
    chat = await event.get_input_chat()
    async with client.conversation(chat) as conver:
        if event.data.decode("UTF-8") == "/download_video":
            await conver.send_message("Enter your video url:")
            respon = await conver.get_response()
            user.url = respon.text
            downloaded_file = await user.download_video()

            if downloaded_file.filesize_mb > 50:

                upload_file = await client.upload_file(f"video.mp4",
                                                       progress_callback=user.on_progress,
                                                       part_size_kb=512)

                await client.send_file(chat, upload_file)
            else:
                await client.send_file(chat, f"video.mp4")
            remove(f"video.mp4")
        elif event.data.decode("UTF-8") == "/extract_audio":
            await conver.send_message("Enter the url of video where is an audio")
            response = await conver.get_response()
            user.url = response.text
            get_audio = await user.download_audio()
            if get_audio.filesize_mb > 50:
                upload_file = await client.upload_file(f"{get_audio.title}.mp3", progress_callback=user.on_progress,
                                                       part_size_kb=512)

                await client.send_file(chat, upload_file)
            else:
                await client.send_file(chat, f"{get_audio.title}.mp3")
        elif event.data.decode("UTF-8") == "/extract_captions":
            await conver.send_message("Enter the url of the video which has a captions: ")
            response = await conver.get_response()
            user.url = response.text
            keyboard = [Button.text(lang) for lang in ["en-US", "ru", "it-IT", " de-DE", "fr-FR"]]
            await conver.send_message("Enter the language of video in code's mapping: ", buttons=keyboard)
            response = await conver.get_response()
            get_video = await user.download_video()
            language_code = response.text
            text = extract_text("video.mp4", language_code)
            remove("video.mp4")
            await client.send_file(chat, text)
            remove(text)


if __name__ == "__main__":
    client.start(bot_token=config.TOKEN)
    client.run_until_disconnected()