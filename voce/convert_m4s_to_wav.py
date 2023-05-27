from pydub import AudioSegment

def convert_m4a_to_wav(m4a_file, wav_file):
    # Load the .m4a file
    audio = AudioSegment.from_file(m4a_file, format='m4a')

    # Export the audio as .wav file
    audio.export(wav_file, format='wav')

# Example usage
m4a_file = r'voce\jos.m4a'
wav_file = r'voce\jos.wav'
convert_m4a_to_wav(m4a_file, wav_file)

m4a_file = r'voce\sus.m4a'
wav_file = r'voce\sus.wav'
convert_m4a_to_wav(m4a_file, wav_file)
