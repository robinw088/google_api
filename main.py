from flask import Flask,render_template,flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import FileField,SubmitField
from flask_wtf.file import FileRequired, FileAllowed
from werkzeug.utils import secure_filename
import pdfplumber
from google.cloud import texttospeech
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = '/Users/Meng/Documents/credentials.json'
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

class PDFForm(FlaskForm):
    pdf = FileField('Please upload a PDF File',validators=[FileRequired(), FileAllowed(['pdf'],"Only PDF Files Allowed")])
    submit=SubmitField('Submit')

app=Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['CKEDITOR_PKG_TYPE'] = 'standard'


@app.route('/', methods=['GET', 'POST'])
def home():
    form=PDFForm()
    text=""
    if form.validate_on_submit():
        f = form.pdf.data
        filename = secure_filename(f.filename)
        f.save(os.path.join(
            './uploads/', filename
        ))
        flash(f'You were successfully upload {filename}')
        with pdfplumber.open(filename) as pdf:
            for page in pdf.pages:
                text+=page.extract_text()
        TexttoSpeech(text,filename)
        audiofile=f'audio/{filename}.mp3'
        return render_template('index.html', audio=True, audiofile=audiofile, form=form)

    return render_template('index.html', form=form)


if __name__=='__main__':
    app.run(debug=True)