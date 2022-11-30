from django.shortcuts import render
from .eng_spellcheck import correct_spelling
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='login')
def spellcheck(request):

    corrected_text = ""
    errors = {
        "lang": False,
        "text": False,
        "audio": False,
        "file": False
    }

    
    if request.method=="POST":
        language = request.POST.get('language')

        text_to_check = request.POST.get('text_to_check')
        errors['text'] = True



        text_to_check = "whereis th elove hehad dated forImuch of thepast who couqdn'tread in sixtgrade and ins pired him"

        if language=="eng":
            corrected_text = correct_spelling(text_to_check)
            corrected_text = corrected_text[0].term.capitalize()
        else:
            corrected_text = "hindi"

        request.session['corrected_text'] = corrected_text
    
    return render(request, "spellcheck/spellcheck.html", {"corrected_text": corrected_text})

def pdf(request):
    corrected_text = request.session.get('corrected_text')
    context = {
        "toolname": "Spelling Correction",
        "corrected_text": corrected_text,
    }
    print(context)
    return render(request, "home/generatepdf.html", context)