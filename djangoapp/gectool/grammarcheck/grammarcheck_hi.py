# import pandas as pd
from googletrans import Translator

translator = Translator()


def correct_grammar_hindi(text_to_check):
    hin_to_eng = translator.translate(text_to_check).text
    result = translator.translate(hin_to_eng, src='en', dest='hi').text
    
    return result