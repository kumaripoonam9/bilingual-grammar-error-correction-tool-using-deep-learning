import phunspell

pspell = phunspell.Phunspell('hi_IN')
# print(pspell.lookup("phunspell"))  # False
# print(pspell.lookup("about"))  # True

# mispelled = pspell.lookup_list("Bill's TV is borken".split(" "))
# print(mispelled)  # ["borken"]

def hi_spellcheck(text):
    # बहूत
    # त्यौहार
    # ऊत्तर दिशा 
    # बहूत जंगल ऊत्तर दिशा में है
    suggestions = pspell.suggest(text)
    # print(type(suggestions))
    suggestions = list(suggestions)
    # for suggestion in suggestions:
    #     print(suggestion)  # Hunspell
    return suggestions
