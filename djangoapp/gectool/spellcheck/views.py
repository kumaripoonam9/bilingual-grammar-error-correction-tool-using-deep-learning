from django.shortcuts import render
from .eng_spellcheck import correct_spelling
from .hi_spellcheck import hi_spellcheck
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from textblob import TextBlob
from langdetect import detect


import phunspell
# Create your views here.

@login_required(login_url='login')
def spellcheck(request):

    corrected_text = ""
    error = 0
    sentence = 1
    
    if request.method=="POST":
        lang_by_user = request.POST.get('lang_by_user')
        # print(lang_by_user)

        text_to_check = request.POST.get('text_to_check')
        # errors['text'] = True

        # no_of_suggestions = 1
        # sentence = 1

        lang_detected = detect(text_to_check)
        lang_detected = lang_detected.split(" ")[0]

        # text_to_check = "whereis th elove hehad dated forImuch of thepast who couqdn'tread in sixtgrade and ins pired him"
        print(lang_by_user, lang_detected)
        # if lang_by_user=="en" and lang_by_user==lang_detected:
        if lang_by_user=="en" and lang_detected!=lang_by_user or lang_by_user=="hi" and lang_detected=="en":
            error = 1
        else:
            if lang_by_user=="en":
                corrected_text = correct_spelling(text_to_check)
                print(corrected_text)
                corrected_text = corrected_text[0].term.capitalize()
                print(corrected_text)

            else:
                # no_of_suggestions = 2
                pspell = phunspell.Phunspell('hi_IN')
                text_to_check = text_to_check.split(" ")

                print(text_to_check)

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
                            print("incorrect w:", t)
                            ct = hi_spellcheck(t)
                            corrected_text += ct[0]
                        # elif t=="।":
                        #     corrected_text += t
                        else:
                            print("correct w:", t)
                            corrected_text += t
                        corrected_text += " "
                # print(corrected_text)
        request.session['corrected_text'] = corrected_text
    
    return render(request, "spellcheck/spellcheck.html", {"corrected_text": corrected_text, "sentence":sentence, "error":error})

def pdf(request):
    corrected_text = request.session.get('corrected_text')
    context = {
        "toolname": "Spelling Correction",
        "corrected_text": corrected_text,
    }
    print(context)
    return render(request, "home/generatepdf.html", context)