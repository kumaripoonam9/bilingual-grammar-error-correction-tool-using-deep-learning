from django.shortcuts import render
from .spellcheck import correct_spelling
from django.http import HttpResponse

# Create your views here.
def spellcheck(request):
    global corrected_text

    corrected_text = ""
    
    if request.method=="POST":
        text_to_check = request.POST.get('text_to_check')
        corrected_text = correct_spelling(text_to_check)
        corrected_text = corrected_text[0].term.capitalize()
    
    return render(request, "spellcheck/spellcheck.html", {"corrected_text": corrected_text})

def pdf(request):
    context = {
        "toolname": "Spelling Correction",
        # "corrected_text": corrected_text,
        "name": 'poonam'
    }
    print(context)
    return render(request, "home/generatepdf.html", context)