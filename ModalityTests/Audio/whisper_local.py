import whisper

file = "/Users/victorbjorkgren/Desktop/New Recording.m4a"


model = whisper.load_model("turbo")
result = model.transcribe(file)
print('LOCAL TRANSCRIPTION')
print(result.keys())
