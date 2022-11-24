from django.shortcuts import render
# from .grammarcheck import correct_grammar

# Create your views here.
def spellcheck(request):
    corrected_text = ""
    
    # if request.method=="POST":
    #     text_to_check = request.POST.get('text_to_check')
    #     corrected_text = correct_grammar(text_to_check, 1)
    #     corrected_text = corrected_text[0]
    
    return render(request, "spellcheck/spellcheck.html", {"corrected_text": corrected_text})