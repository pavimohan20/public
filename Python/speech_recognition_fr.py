import speech_recognition as sr

# Initialize recognizer
recognizer = sr.Recognizer()

# Path to the audio file
audio_file_path = "D:\Documents\On dit.WAV"

# Convert the WAV file to text
with sr.AudioFile(audio_file_path) as source:
    audio_data = recognizer.record(source)
    text = recognizer.recognize_google(audio_data, language='fr-FR')

print(text)
