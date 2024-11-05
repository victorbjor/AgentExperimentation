from openai import OpenAI
client = OpenAI()

file = "/Users/victorbjorkgren/Desktop/New Recording.m4a"

audio_file= open(file, "rb")
transcription = client.audio.transcriptions.create(
    model="whisper-1",
    file=audio_file
)
print('API TRANSCRIPTION')
print(transcription.text)

import whisper

model = whisper.load_model("turbo")
result = model.transcribe(file)
print('LOCAL TRANSCRIPTION')
print(result["text"])
