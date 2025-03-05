import speech_recognition as sr
import pyttsx3


def transcribe_voice_to_text():
    # Initialize the recognizer
    recognizer = sr.Recognizer()

    # Use the microphone as the audio source
    with sr.Microphone() as source:
        print("Listening... (Press Ctrl+C to stop)")

        while True:
            try:
                # Adjust for ambient noise
                recognizer.adjust_for_ambient_noise(source)
                # Listen for audio
                audio = recognizer.listen(source)

                print("Transcribing...")
                # Use Google Web Speech API to transcribe
                text = recognizer.recognize_google(audio)
                print("You said: " + text)



            except sr.UnknownValueError:
                print("Sorry, I could not understand the audio.")
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")
            except KeyboardInterrupt:
                print("Stopping the transcription.")
                break


 # Example usage
# if __name__ == "__main__":
#     text_to_convert = "Hello, this is a text-to-speech conversion."
#     text_to_voice(text_to_convert, play_audio=True)
# #

from gtts import gTTS
import os
from playsound import playsound  # Optional

def text_to_voice(text, filename='output.mp3', play_audio=False):
    # Initialize the pyttsx3 engine

    # # Create a gTTS object
    tts = gTTS(text=text, lang='en')
    #
    # # Save the audio file
    tts.save(filename)
    print(f"Audio saved as {filename}")

    # Optionally play the audio
    if play_audio:
        playsound(filename)

#
# if __name__ == "__main__":
#     transcribe_voice_to_text("transcription.txt")




def text_to_voice_rev1(text, filename='output.mp3', play_audio=False, voice_id=None):
    # Initialize the pyttsx3 engine
    engine = pyttsx3.init()

    # Set voice if voice_id is provided
    if voice_id is not None:
        engine.setProperty('voice', voice_id)

    # Save the audio to a file
    engine.save_to_file(text, filename)
    engine.runAndWait()

    print(f"Audio saved as {filename}")

    # Optionally play the audio
    if play_audio:
        import playsound
        playsound.playsound(filename)

# Example usage
if __name__ == "__main__":
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')

    # Print available voices
    for index, voice in enumerate(voices):
        print(f"Voice {index}: {voice.name} - {voice.languages}")

    # Set the desired voice_id (e.g., 0 for the first voice)
    desired_voice_id = voices[17].id  # Change the index as needed

    text_to_voice_rev1("Hello, how are you?", voice_id=desired_voice_id)