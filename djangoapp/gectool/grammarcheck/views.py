from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .grammarcheck import correct_grammar
from langdetect import detect

# Create your views here.
@login_required(login_url='login')
def grammarcheck(request):
    corrected_text = ""
    error = 0

    # speech to text
    # if request.GET.get('audio_btn'):
    #     print("audio")

    if request.method=="POST":
        language = request.POST.get('language')
        text_to_check = request.POST.get('text_to_check')

        text_to_check = text_to_check.replace("\n"," ")

        lang_detected = detect(text_to_check)

        text_to_check = text_to_check.split(".")

        if lang_detected!=language:
            error = 1
        else:
            if language=="en":
                for t in text_to_check:
                    ct = correct_grammar(t.strip(), 1)[0]
                    # corrected_text += ct.capitalize()
                    corrected_text += ct
                    corrected_text += " "
            else:
                corrected_text = "hindi model not implemented"

    request.session['corrected_text'] = corrected_text

    return render(request, "grammarcheck/grammarcheck.html", {"corrected_text": corrected_text, "error":error})


def pdf(request):
    corrected_text = request.session.get('corrected_text')
    context = {
        "toolname": "Grammar Correction",
        "corrected_text": corrected_text,
    }
    print(context)
    return render(request, "home/generatepdf.html", context)