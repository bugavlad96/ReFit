import pyttsx3

def speak(text, output_file):
    engine = pyttsx3.init()

    # Set the output file path and format
    engine.save_to_file(text, output_file)
    
    # Speak the text
    engine.runAndWait()

# Example usage
text = "repede sus"
output_file = r"tests\voice_tests\sus.wav"
speak(text, output_file)

# Example usage
text = "incet in jos"
output_file = r"tests\voice_tests\jos.wav"
speak(text, output_file)