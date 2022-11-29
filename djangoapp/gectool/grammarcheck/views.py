from django.shortcuts import render
from .grammarcheck import correct_grammar

# Create your views here.
def grammarcheck(request):
    corrected_text = ""
    errors = {
        "lang": False,
        "text": False,
        "audio": False,
        "file": False
    }

    # speech to text
    # if request.GET.get('audio_btn'):
    #     print("audio")

    if request.method=="POST":
        language = request.POST.get('language')
        text_to_check = request.POST.get('text_to_check')

        text_to_check = text_to_check.replace("\n","")
        text_to_check = text_to_check.split(".")

        if language=="eng":
            for t in text_to_check:
                corrected_text += correct_grammar(t.strip(), 1)[0]
                corrected_text += " "
        else:
            corrected_text = "hindi"

        corrected_text = corrected_text.capitalize()
    
    return render(request, "grammarcheck/grammarcheck.html", {"corrected_text": corrected_text})