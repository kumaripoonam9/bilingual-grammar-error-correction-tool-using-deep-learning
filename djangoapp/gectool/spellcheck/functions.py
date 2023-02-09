# import argparse
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
import torch
# import soundfile as sf
import PyPDF2
import docx
import librosa
import speech_recognition as sr


def handle_uploaded_file(f):
    ext = f.name.split('.')[-1]
    with open('static/upload/file.'+ext, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return ext


# for .txt files
def txtToText(filename):
    with open(filename, encoding="utf8") as f:
        contents = f.read()
        # result = contents.replace('\n', ' ')
        return contents


# for .docx files
def docxToText(filename):
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    x = '\n'.join(fullText)
    return x


# for .pdf
def pdfToText(filename):
    # creating a pdf file object
    pdfFileObj = open(filename, 'rb')

    # creating a pdf reader object
    pdfReader = PyPDF2.PdfReader(pdfFileObj)

    # printing number of pages in pdf file
    # print(len(pdfReader.pages))

    final_text = []
    for page in range(len(pdfReader.pages)):
        # print(page)
        pageObj = pdfReader.pages[page]
        text = pageObj.extract_text()
        final_text.append(text)
        # pdfFileObj.close()

    result = " ".join(final_text)
    # result = result.replace('\n', '')

    return result

# creating a page object
# pageObj = pdfReader.pages[:7]

# extracting text from page
# print(pageObj.extract_text())

# closing the pdf file object
# pdfFileObj.close()


# load pretrained model for HINDI
processor = Wav2Vec2Processor.from_pretrained(
    "Harveenchadha/vakyansh-wav2vec2-hindi-him-4200")
model = Wav2Vec2ForCTC.from_pretrained(
    "Harveenchadha/vakyansh-wav2vec2-hindi-him-4200")

def parse_transcription(wav_file):
    # downsample it to 16kHz
    audio_input, sample_rate = librosa.load(wav_file, sr = 16000)

    # load audio
    # audio_input, sample_rate = sf.read(wav_file)

    # pad input values and return pt tensor
    input_values = processor(
        audio_input, sampling_rate=sample_rate, return_tensors="pt").input_values

    # INFERENCE
    # retrieve logits & take argmax
    logits = model(input_values).logits
    predicted_ids = torch.argmax(logits, dim=-1)

    # transcribe
    transcription = processor.decode(
        predicted_ids[0], skip_special_tokens=True)
    # print(transcription)

    return transcription


r = sr.Recognizer()
def parse_transcription_eng(wav_file):
    a = sr.AudioFile(wav_file)
    with a as source:
        audio = r.record(source)

    return r.recognize_google(audio)
