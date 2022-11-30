from django.shortcuts import render
# from .grammarcheck import correct_grammar
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='login')
def summarizer(request):
    corrected_text = ""
    
    # if request.method=="POST":
    #     text_to_check = request.POST.get('text_to_check')
    #     corrected_text = correct_grammar(text_to_check, 1)
    #     corrected_text = corrected_text[0]
    
    return render(request, "summarizer/summarizer.html", {"corrected_text": corrected_text})