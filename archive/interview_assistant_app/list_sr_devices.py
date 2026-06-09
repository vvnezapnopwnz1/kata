import speech_recognition as sr

print("SpeechRecognition sees the following devices:")
for index, name in enumerate(sr.Microphone.list_microphone_names()):
    print(f"Index {index}: {name}")
