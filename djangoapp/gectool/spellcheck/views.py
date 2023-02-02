from django.shortcuts import render
from .eng_spellcheck import correct_spelling
from .hi_spellcheck import hi_spellcheck
from .forms import FileUploadForm
from .functions import handle_uploaded_file, txtToText, docxToText, pdfToText
from django.contrib.auth.decorators import login_required
from langdetect import detect
import phunspell
import aspose.words as aw



@login_required(login_url='login')
def spellcheck(request):

    corrected_text = ""
    error = 0
    sentence = 1
    text_to_check = ""
    
    if request.method=="POST":

        if 'textarea_form_button' in request.POST:
            # print("textarea_form_button")

            lang_by_user = request.POST.get('lang_by_user')
            text_to_check = request.POST.get('text_to_check')

            lang_detected = detect(text_to_check)
            lang_detected = lang_detected.split(" ")[0]

            # text_to_check = "whereis th elove hehad dated forImuch of thepast who couqdn'tread in sixtgrade and ins pired him"
            # print(lang_by_user, lang_detected)
            # if lang_by_user=="en" and lang_by_user==lang_detected:
            if lang_by_user=="en" and lang_detected!=lang_by_user or lang_by_user=="hi" and lang_detected=="en":
                error = 1
            else:
                if lang_by_user=="en":
                    text_to_check = text_to_check.split("\n")
                    for t in text_to_check:
                        if t!="\r":
                            t = t.split(".")
                            for x in t:
                                ct = correct_spelling(x)
                                # print(corrected_text)
                                ct = ct[0].term.capitalize()
                                corrected_text = corrected_text + ct + ". " 
                        corrected_text = corrected_text + "\n"
                    print(corrected_text)
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

                text_to_check = text_to_check.split("\n")
                print(text_to_check)
                for t in text_to_check:
                    if t!="" and t!=" " and t.isspace()!=True:
                        t = t.split(".")
                        for x in t:
                            ct = correct_spelling(x)
                            ct = ct[0].term.capitalize()
                            corrected_text = corrected_text + ct + ". " 
                    corrected_text = corrected_text + "\n"
                print(corrected_text)
        elif 'audio_form_button' in request.POST:
            print("audio_form_button")

        request.session['corrected_text'] = corrected_text

    else:
        file_form = FileUploadForm()
    

    return render(request, "spellcheck/spellcheck.html", {"corrected_text": corrected_text, 
    "sentence":sentence, 
    "error":error,
    "file_form": file_form})



def pdf(request):
    corrected_text = request.session.get('corrected_text')
    context = {
        "toolname": "Spelling Correction",
        "corrected_text": corrected_text,
    }
    # print(context)
    return render(request, "home/generatepdf.html", context)