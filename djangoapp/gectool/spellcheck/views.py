from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .eng_spellcheck import correct_spelling
from .hi_spellcheck import hi_spellcheck

from .forms import FileUploadForm

from .functions import handle_uploaded_file, txtToText, docxToText, pdfToText, parse_transcription, parse_transcription_eng

from langdetect import detect
import phunspell
import aspose.words as aw
import os, time, json



@login_required(login_url='login')
def spellcheck(request):

    corrected_text = ""
    error = 0
    error_text = ""
    sentence = 1
    text_to_check = ""
    text_to_check_eng = ""
    text_to_check_hi = ""
    original_text = ""

    tab = 1

    file_form = FileUploadForm()
    
    if request.method=="POST":

        if 'textarea_form_button' in request.POST:

            lang_by_user = request.POST.get('lang_by_user')
            if lang_by_user == 'en':
                text_to_check = request.POST.get('text_to_check_eng')
                text_to_check_eng = text_to_check
                text_to_check_hi = ""
            else:
                text_to_check = request.POST.get('text_to_check_hi')
                text_to_check_hi = text_to_check
                text_to_check_eng = ""
            original_text = text_to_check

            if text_to_check == "" or text_to_check == False:
                error = 1
                if lang_by_user=='en':
                    error_text = "Please type something in the english textarea"
                else:
                    error_text = "Please type something in the hindi textarea"
            else:
                # lang_detected = detect(text_to_check)
                # print("lang_detected = ", lang_detected)
                # lang_detected = lang_detected.split(" ")[0]

                # if lang_by_user=="en" and lang_detected!=lang_by_user or lang_by_user=="hi" and lang_detected=="en":
                #     error = 1
                #     error_text = "Language from input and language selected by user don't match!"
                # else:
                if lang_by_user=="en":
                    text_to_check = text_to_check.split("\n")
                    # print(text_to_check)
                    for t in text_to_check:
                        if t!="\r":
                            t = t.split(".")
                            t = list(filter(None, t))
                            print(t)
                            for x in t:
                                # print(x.isupper())
                                # if x.isupper():
                                #     # print(x)
                                #     ct = x
                                # else:
                                ct = correct_spelling(x)
                                # print(corrected_text)
                                ct = ct[0].term.capitalize()
                                corrected_text = corrected_text + ct + ". " 
                        corrected_text = corrected_text + "\n"
                    # print(corrected_text)
                else:
                    # no_of_suggestions = 2
                    pspell = phunspell.Phunspell('hi_IN')
                    text_to_check = text_to_check.split(" ")

                    # print(text_to_check)

                    if len(text_to_check)==1:
                        if pspell.lookup(text_to_check[0]):
                            corrected_text = "शब्द पहले से ही सही है।"
                        else:
                            sentence = 0
                            corrected_text = hi_spellcheck(text_to_check[0])
                            corrected_text = '\n'.join(corrected_text)
                    else:
                        for t in text_to_check:
                            if t=="।":
                                corrected_text += t
                            elif not pspell.lookup(t):
                                # print("incorrect w:", t)
                                ct = hi_spellcheck(t)
                                corrected_text += ct[0]
                            # elif t=="।":
                            #     corrected_text += t
                            else:
                                # print("correct w:", t)
                                corrected_text += t
                            corrected_text += " "

            # creating forms for audio and file upload
            file_form = FileUploadForm()
        
        elif 'file_form_button' in request.POST:

            tab=3
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

                original_text = text_to_check
                # print(text_to_check)

                # text corections
                if lang_detected =="en":
                    text_to_check = text_to_check.split("\n")
                    # print(text_to_check)
                    for t in text_to_check:
                        # if t!="" and t!=" " and t.isspace()!=True:
                        t = t.split(".")
                        t = list(filter(None, t))
                        # print(t)
                        for x in t:
                            x = x.strip()
                            print(x)
                            if x:
                            # if x.isupper():
                            #     ct = x
                            # else:
                                ct = correct_spelling(x)
                                ct = ct[0].term.capitalize()
                                corrected_text = corrected_text + ct + ". " 
                        corrected_text = corrected_text + "\n"
                else:
                    text_to_check = text_to_check.split("\n")[0]
                    # no_of_suggestions = 2
                    pspell = phunspell.Phunspell('hi_IN')
                    text_to_check = text_to_check.split(" ")
                    # print(text_to_check)
                    if len(text_to_check)==1:
                        if pspell.lookup(text_to_check[0]):
                            corrected_text = "शब्द पहले से ही सही है।"
                        else:
                            sentence = 0
                            corrected_text = hi_spellcheck(text_to_check[0])
                    else:
                        for t in text_to_check:
                            if t=="।":
                                corrected_text += t
                            elif not pspell.lookup(t):
                                # print("incorrect w:", t)
                                ct = hi_spellcheck(t)
                                corrected_text += ct[0]
                            # elif t=="।":
                            #     corrected_text += t
                            else:
                                # print("correct w:", t)
                                corrected_text += t
                            corrected_text += " "
                # os.remove(filename)
                # print(corrected_text)

        elif 'audio_form_button' in request.POST:
            tab=2
            lang_by_user = request.POST.get('lang_by_user')
            filepath = 'spellcheck/audio/gec_speech_record.wav'

            if os.path.exists(filepath):
                if lang_by_user=="hi":
                    text_to_check = parse_transcription(filepath)
                    # pspell = phunspell.Phunspell('hi_IN')
                    # for t in text_to_check:
                    #     if not pspell.lookup(t):
                    #         # print("incorrect w:", t)
                    #         ct = hi_spellcheck(t)
                    #         corrected_text += ct[0]
                    #     # elif t=="।":
                    #     #     corrected_text += t
                    #     else:
                    #         # print("correct w:", t)
                    #         corrected_text += t
                    #     corrected_text += " "
                else:
                    text_to_check = parse_transcription_eng(filepath)
                    # corrected_text = text_to_check

                corrected_text = text_to_check
                original_text = "Audio recorded"
                os.remove(filepath)
            else:
                error = 1
                error_text = "First record the audio"

            # creating file form
            file_form = FileUploadForm()
        
        print(corrected_text)

        request.session['corrected_text'] = corrected_text
        request.session['toolname'] = "Spelling Correction"

    else:
        file_form = FileUploadForm()

    context = {
        "corrected_text": corrected_text, 
        "sentence":sentence, 
        "error":error,
        "error_text": error_text,
        "file_form": file_form,
        "original_text": original_text,
        'text_to_check_eng': text_to_check_eng,
        'text_to_check_hi': text_to_check_hi,
        'tab': tab,
    }
    return render(request, "spellcheck/spellcheck.html", context)


@login_required(login_url='login')
def pdf(request):
    corrected_text = request.session.get('corrected_text')
    toolname = request.session.get('toolname')
    context = {
        "toolname": toolname,
        "corrected_text": corrected_text,
    }
    # print(context)
    return render(request, "home/generatepdf.html", context)



# audio upload to server
@csrf_exempt
def upload_driver(request):
    upload_file = request.FILES['audio_data']
    ret = {} 
    if upload_file:
        target_folder = 'spellcheck/audio/gec_speech_record.wav'

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

