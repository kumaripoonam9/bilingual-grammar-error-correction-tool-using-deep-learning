from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from langdetect import detect
import aspose.words as aw
import os, time

from spellcheck.forms import FileUploadForm
from spellcheck.functions import handle_uploaded_file, txtToText, docxToText, pdfToText, parse_transcription, parse_transcription_eng

from .summarizer_eng import eng_summary
from .summarizer_hi import hi_summary



@login_required(login_url='login')
def summarizer(request):

    summary = ""
    error = 0
    error_text = ""
    sentence = 1
    text = ""
    original_text = ""
    
    if request.method=="POST":

        lang_by_user = request.POST.get('lang_by_user')

        if 'textarea_form_button' in request.POST:

            if lang_by_user == 'en':
                text = request.POST.get('text_to_check_eng')
            else:
                text = request.POST.get('text_to_check_hi')
            original_text = text
            if text == "" or text == False:
                error = 1
                error_text = "Please type something"
            else:
                # text = request.POST.get('text_to_check')
                text = text.replace("\n"," ")
                text = text.replace("\r","")
                
                # print(text)

                lang_detected = detect(text)
                print(lang_detected)
                lang_detected = lang_detected.split(" ")[0]

                # text = text.split(".")

                if lang_by_user=="en" and lang_detected!=lang_by_user or lang_by_user=="hi" and lang_detected=="en":
                    error = 1
                    error_text = "Language from input and language selected by user don't match!"
                else:
                    if lang_by_user=="en":
                        summary = eng_summary(text)
                        # print(type(summary), summary)
                    else:
                        summary = hi_summary(text)
                        # print(type(summary), summary)

            # creating forms for audio and file upload
            file_form = FileUploadForm()
        
        elif 'file_form_button' in request.POST:

            file_form = FileUploadForm(request.POST, request.FILES)
            if file_form.is_valid():
                ext = handle_uploaded_file(request.FILES['file'])
                filename = './static/upload/file.'+ext
                # checkiing extensions
                if ext=='txt':
                    text = txtToText(filename)
                elif ext=='docx':
                    text = docxToText(filename)
                elif ext=='doc':
                    doc = aw.Document(filename)
                    filename = './static/upload/file.docx'
                    doc.save(filename)
                    text = docxToText(filename)
                elif ext=='pdf':
                    text = pdfToText(filename)

                lang_detected = detect(text)
                lang_detected = lang_detected.split(" ")[0]

                # print(text)
                original_text = text
                text = text.replace("\n"," ")
                text = text.replace("\r","")

                if lang_by_user=="en":
                    # text = text.replace("\n"," ")
                    # text = text.replace("\r","")
                    summary = eng_summary(text)
                else:
                    # text = text.split("।")
                    # text = text.replace("\n"," ")
                    # text = text.replace("\r","")
                    summary = hi_summary(text)
                    # summary = "hindi model not implemented"
               
                print(summary)

        elif 'audio_form_button' in request.POST:
            lang_by_user = request.POST.get('lang_by_user')
            filepath = 'summarizer/audio/gec_speech_record.wav'

            if os.path.exists(filepath):
                if lang_by_user=="hi":
                    text = parse_transcription(filepath) + "।"
                    text = text.replace("\n"," ")
                    text = text.replace("\r","")
                    print(text)
                    summary = hi_summary(text)
                else:
                    text = parse_transcription_eng(filepath)
                    summary = eng_summary(text)
                original_text = "Audio recorded"
                os.remove(filepath)
            else:
                error = 1
                error_text = "First record the audio"

            # creating file form
            file_form = FileUploadForm()

        request.session['corrected_text'] = summary
        request.session['toolname'] = "Text Summary"

    else:
        file_form = FileUploadForm()

    context = {
        "summary": summary, 
        "sentence":sentence, 
        "error":error,
        "error_text": error_text,
        "file_form": file_form,
        "original_text": original_text
    }
    return render(request, "summarizer/summarizer.html", context)



# audio upload to server
@csrf_exempt
def upload_driver(request):
    upload_file = request.FILES['audio_data']
    ret = {} 
    if upload_file:
        target_folder = 'summarizer/audio/gec_speech_record.wav'

        rtime = str(int(time.time()))

        filename = request.POST.get('filename', False)
        blob = request.POST.get('blob', False)

        with open(target_folder, 'wb+') as dest:
            for c in upload_file.chunks():
                dest.write(c)
        ret['file_remote_path'] = target_folder
    else:
        return HttpResponse(status=500)
    
    # return HttpResponse(json.dumps(ret), mimetype = "application/json")
    return render(request, "summarizer/summarizer.html")
