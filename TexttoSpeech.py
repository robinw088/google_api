
from google.cloud import texttospeech
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = '/Users/Meng/documents/credentials.json'
# Instantiates a client
class TexttoSpeech:
    def __init__(self, text, filename):
        self.text=text
        self.filename=filename
        self.client = texttospeech.TextToSpeechClient()
        self.synthesis_input = texttospeech.SynthesisInput(text=self.text)

    # Set the text input to be synthesized


    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
        self.voice = texttospeech.VoiceSelectionParams(
            language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
        )

    # Select the type of audio file you want returned
        self.audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
        )

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
        self.response = self.client.synthesize_speech(
            input=self.synthesis_input, voice=self.voice, audio_config=self.audio_config)

    # The response's audio_content is binary.
        with open(f"./static/audio/{filename}.mp3", "wb") as out:
            # Write the response to the output file.
            out.write(self.response.audio_content)