import pyttsx3

def speak(text):
    engine = pyttsx3.init()

    # Get the available voices
    voices = engine.getProperty('voices')

    # # Print available voices
    # for voice in voices:
    #     print("Voice ID:", voice.id)
    #     print("Voice Name:", voice.name)
    #     print("Languages Spoken:", voice.languages)
    #     print("----------")

    # Select the voice you want to use
    voice_id = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0'  # Replace 'voice_id' with the desired voice ID from the available voices

    # Set the voice
    engine.setProperty('voice', voice_id)
    

    # Speak the text
    engine.say(text)
    engine.runAndWait()

# # Example usage
# text = "Hello, how are you?"
# speak(text)
