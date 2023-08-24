import speech_recognition
from pydub import AudioSegment
from os import getcwd, listdir, remove
from subprocess import run
import pyaudio

current_directory = getcwd()


def extract_text(video, language_code):
    text = ""
    recognizer = speech_recognition.Recognizer()
    run(f"ffmpeg -i {video} -vn soundtrack.wav")
    audiofile = AudioSegment.from_file("soundtrack.wav", format="wav")
    if audiofile.duration_seconds / 60 > 1:
        for i, chunk in enumerate(audiofile[::60_000]):
            chunk.export(f"soundtrack_part_{i}.wav", format="wav")
        remove("soundtrack.wav")
        duration = 0.00
        try:
            print("Extracting text is starting!")
            for file in listdir(current_directory):
                if "soundtrack" in file:
                    with speech_recognition.AudioFile(file) as source:
                        audio = recognizer.record(source)
                        print(duration)
                        text += f"from {duration} to {duration + round(source.DURATION / 60, 2)}: " + str(
                            recognizer.recognize_google(
                                audio, language=language_code)) + "\n"
                        duration += round(source.DURATION / 60, 2)
                    remove(file)
        except Exception as exce:
            print("Extracting failed!!!")
            print(exce.__repr__())

    else:
        with speech_recognition.AudioFile(video) as audiofile:
            audio = recognizer.record(audiofile)
            text = recognizer.recognize_google(audio, language=language_code)
        remove(video)
    with open("captions.txt", "w") as file:
        file.write(text)
    return "captions.txt"
