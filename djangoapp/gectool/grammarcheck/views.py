from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .grammarcheck_eng import correct_grammar_eng
from .grammarcheck_hi import correct_grammar_hindi

from langdetect import detect
import aspose.words as aw
import os, time

from spellcheck.forms import FileUploadForm
from spellcheck.functions import handle_uploaded_file, txtToText, docxToText, pdfToText, parse_transcription, parse_transcription_eng



@login_required(login_url='login')
def grammarcheck(request):

    corrected_text = ""
    error = 0
    error_text = ""
    sentence = 1
    text_to_check = ""
    original_text = ""
    
    if request.method=="POST":

        lang_by_user = request.POST.get('lang_by_user')

        if 'textarea_form_button' in request.POST:

            if lang_by_user == 'en':
                text_to_check = request.POST.get('text_to_check_eng')
            else:
                text_to_check = request.POST.get('text_to_check_hi')
            
            original_text = text_to_check

            if text_to_check == "" or text_to_check == False:
                error = 1
                error_text = "Please type something"
            else:
                # lang_by_user = request.POST.get('lang_by_user')
                # text_to_check = request.POST.get('text_to_check')

                text_to_check = text_to_check.replace("\n"," ")

                lang_detected = detect(text_to_check)
                lang_detected = lang_detected.split(" ")[0]

                if lang_by_user=="en" and lang_detected!=lang_by_user or lang_by_user=="hi" and lang_detected=="en":
                    error = 1
                    error_text = "Language from input and language selected by user don't match!"
                else:
                    if lang_by_user=="en":
                        text_to_check = text_to_check.split(".")
                        for t in text_to_check:
                            ct = correct_grammar_eng(t.strip(), 1)[0]
                            # corrected_text += ct.capitalize()
                            corrected_text += ct
                            corrected_text += " "
                        print(corrected_text)
                    else:
                        corrected_text = correct_grammar_hindi(text_to_check)

            # creating forms for audio and file upload
            file_form = FileUploadForm()
        
        elif 'file_form_button' in request.POST:

            file_form = FileUploadForm(request.POST, request.FILES)
            if file_form.is_valid():
                ext = handle_uploaded_file(request.FILES['file'])
                filename = './static/upload/file.'+ext
                # checkiing extensions
                if ext=='txt':
                    text_to_check = txtToText(filename)
                elif ext=='docx':
                    text_to_check = docxToText(filename)
                elif ext=='doc':
                    doc = aw.Document(filename)
                    filename = './static/upload/file.docx'
                    doc.save(filename)
                    text_to_check = docxToText(filename)
                elif ext=='pdf':
                    text_to_check = pdfToText(filename)

                lang_detected = detect(text_to_check)
                lang_detected = lang_detected.split(" ")[0]

                if lang_by_user != lang_detected:
                    error = 1
                    error_text = "Input language and uploaded file language don't match"
                else:
                    print(text_to_check)
                    original_text = text_to_check
                    
                    if lang_by_user=="en":
                        text_to_check = text_to_check.split("\n")
                        text_to_check = list(filter(None, text_to_check))
                    # print(text_to_check)
                        for t in text_to_check:
                            if not t.isspace():
                                t = t.split(".")
                                for x in t:
                                    if not x.isspace():
                                        ct = correct_grammar_eng(x.strip(), 1)[0]
                                        corrected_text += ct
                                        corrected_text += " "
                            corrected_text = corrected_text + "\n"
                        print(corrected_text)
                    else:
                        # text_to_check = text_to_check.replace("\n"," ")
                        corrected_text = correct_grammar_hindi(text_to_check)
                        # corrected_text = "hindi model not implemented"
               
                print(corrected_text)

        elif 'audio_form_button' in request.POST:
            lang_by_user = request.POST.get('lang_by_user')
            filepath = 'grammarcheck/audio/gec_speech_record.wav'

            if os.path.exists(filepath):
                if lang_by_user=="hi":
                    text_to_check = parse_transcription(filepath)
                    corrected_text = correct_grammar_hindi(text_to_check)
                else:
                    text_to_check = parse_transcription_eng(filepath)
                    # corrected_text = correct_grammar_eng(text_to_check, 1)[0]
                    corrected_text = correct_grammar_eng(text_to_check, 1)[0]
                    # corrected_text = "hindi model not implemented"
                original_text = "Audio recorded"
                os.remove(filepath)
            else:
                error = 1
                error_text = "First record the audio"

            # creating file form
            file_form = FileUploadForm()

        request.session['corrected_text'] = corrected_text
        request.session['toolname'] = "Grammar Correction"


    else:
        file_form = FileUploadForm()

    context = {
        "corrected_text": corrected_text, 
        "sentence":sentence, 
        "error":error,
        "error_text": error_text,
        "file_form": file_form,
        "original_text": original_text
    }

    return render(request, "grammarcheck/grammarcheck.html", context)


@login_required(login_url='login')
def pdf(request):
    corrected_text = request.session.get('corrected_text')
    toolname = request.session.get('toolname')
    context = {
        "toolname": toolname,
        "corrected_text": corrected_text,
    }
    print(context)
    return render(request, "home/generatepdf.html", context)


# audio upload to server
@csrf_exempt
def upload_driver(request):
    upload_file = request.FILES['audio_data']
    ret = {} 
    if upload_file:
        target_folder = 'grammarcheck/audio/gec_speech_record.wav'

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
    return render(request, "spellcheck/spellcheck.html")

