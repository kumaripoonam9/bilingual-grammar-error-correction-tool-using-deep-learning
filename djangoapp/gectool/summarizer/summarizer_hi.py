import math

import networkx as nx
import numpy as np

from nltk.tokenize.punkt import PunktSentenceTokenizer
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer

from googletrans import Translator


sentence_tokenizer = PunktSentenceTokenizer()

def textrank(document):
    
    sentences = sentence_tokenizer.tokenize(document)

    bow_matrix = CountVectorizer().fit_transform(sentences)
    normalized = TfidfTransformer().fit_transform(bow_matrix)

    similarity_graph = normalized * normalized.T

    nx_graph = nx.from_scipy_sparse_matrix(similarity_graph)
    scores = nx.pagerank(nx_graph)
    sentence_array = sorted(((scores[i], s) for i, s in enumerate(sentences)), reverse=True)

    print(sentence_array)
        
    sentence_array = np.asarray(sentence_array)

    print(len(sentence_array))
        
    fmax = float(sentence_array[0][0])
    fmin = float(sentence_array[len(sentence_array) - 1][0])
        
    temp_array = []
    # Normalization
    for i in range(0, len(sentence_array)):
        if fmax - fmin == 0:
            temp_array.append(0)
        else:
            temp_array.append((float(sentence_array[i][0]) - fmin) / (fmax - fmin))

            threshold = (sum(temp_array) / len(temp_array)) + 0.2
        
            sentence_list = []

    for i in range(0, len(temp_array)):
        if temp_array[i] > threshold:
            sentence_list.append(sentence_array[i][1])

    seq_list = []
    for sentence in sentences:
        if sentence in sentence_list:
            seq_list.append(sentence+' ')
    
    return seq_list



translator = Translator()

def hi_summary(hinText):

    result = ""

    engText=translator.translate(hinText,src='hi',dest='en')
    engSum=textrank(engText.text)

    for sentence in engSum:
        hinSent = Translator().translate(sentence,src='en',dest='hi')	
        result += hinSent.text	
        # f=open('HindiSum.txt','ab')
        # f.write(temp.encode('utf-8'))
        # f.close()
    
    return result









# import nltk
# from nltk import sent_tokenize, word_tokenize
# from nltk.corpus import stopwords
# from nltk.stem import PorterStemmer
# import math



# # sample text

# # doc="""होली रंगों का एक प्रसिद्ध त्योहार है जो हर साल फागुन के महीने में भारत के लोगों द्वारा बड़ी खुशी के साथ मनाया जाता है। ये ढ़ेर सारी मस्ती और खिलवाड़ का त्योहार है खास तौर से बच्चों के लिये जो होली के एक हफ्ते पहले और बाद तक रंगों की मस्ती में डूबे रहते है। हिन्दु धर्म के लोगों द्वारा इसे पूरे भारतवर्ष में मार्च के महीने में मनाया जाता है खासतौर से उत्तर भारत में।सालों से भारत में होली मनाने के पीछे कई सारी कहानीयाँ और पौराणिक कथाएं है। इस उत्सव का अपना महत्व है, हिन्दु मान्यतों के अनुसार होली का पर्व बहुत समय पहले प्राचीन काल से मनाया जा रहा है जब होलिका अपने भाई के पुत्र को मारने के लिये आग में लेकर बैठी और खुद ही जल गई। उस समय एक राजा था हिरण्यकशयप जिसका पुत्र प्रह्लाद था और वो उसको मारना चाहता था क्योंकि वो उसकी पूजा के बजाय भगवान विष्णु की भक्ती करता था। इसी वजह से हिरण्यकशयप ने होलिका को प्रह्लाद को अपनी गोद में लेकर आग में बैठने को कहा जिसमें भक्त प्रह्लाद तो बच गये लेकिन होलिका मारी गई।जबकि, उसकी ये योजना भी असफल हो गई, क्योंकि वो भगवान विष्णु का भक्त था इसलिये प्रभु ने उसकी रक्षा की। षड़यंत्र में होलिका की मृत्यु हुई और प्रह्लाद बच गया। उसी समय से हिन्दु धर्म के लोग इस त्योहार को मना रहे है। होली से ठीक एक दिन पहले होलिका दहन होता है जिसमें लकड़ी, घास और गाय के गोबर से बने ढ़ेर में इंसान अपने आप की बुराई भी इस आग में जलाता है। होलिका दहन के दौरान सभी इसके चारों ओर घूमकर अपने अच्छे स्वास्थय और यश की कामना करते है साथ ही अपने सभी बुराई को इसमें भस्म करते है। इस पर्व में ऐसी मान्यता भी है कि सरसों से शरीर पर मसाज करने पर उसके सारे रोग और बुराई दूर हो जाती है साथ ही साल भर तक सेहत दुरुस्त रहती है।होलिका दहन की अगली सुबह के बाद, लोग रंग-बिरंगी होली को एक साथ मनाने के लिये एक जगह इकठ्ठा हो जाते है। इसकी तैयारी इसके आने से एक हफ्ते पहले ही शुरु हो जाती है, फिर क्या बच्चे और क्या बड़े सभी बेसब्री से इसका इंतजार करते है और इसके लिये ढ़ेर सारी खरीदारी करते। यहाँ तक कि वो एक हफ्ते पहले से ही अपने दोस्तों, पड़ोसियों और प्रियजनों के साथ पिचकारी और रंग भरे गुब्बारों से खेलना शुरु कर देते। इस दिन लोग एक-दूसरे के घर जाकर रंग गुलाल लगाते साथ ही मजेदार पकवानों का आनंद लेते।

# # होली रंगों का एक प्रसिद्ध त्योहार है जो हर साल फागुन के महीने में भारत के लोगों द्वारा बड़ी खुशी के साथ मनाया जाता है। 

# # ये ढ़ेर सारी मस्ती और खिलवाड़ का त्योहार है खास तौर से बच्चों के लिये जो होली के एक हफ्ते पहले और बाद तक रंगों की मस्ती में डूबे रहते है। 

# # हिन्दु धर्म के लोगों द्वारा इसे पूरे भारतवर्ष में मार्च के महीने में मनाया जाता है खासतौर से उत्तर भारत में।सालों से भारत में होली मनाने के पीछे कई सारी कहानीयाँ और पौराणिक कथाएं है। 

# # इस उत्सव का अपना महत्व है, हिन्दु मान्यतों के अनुसार होली का पर्व बहुत समय पहले प्राचीन काल से मनाया जा रहा है जब होलिका अपने भाई के पुत्र को मारने के लिये आग में लेकर बैठी और खुद ही जल गई। 

# # उस समय एक राजा था हिरण्यकशयप जिसका पुत्र प्रह्लाद था और वो उसको मारना चाहता था क्योंकि वो उसकी पूजा के बजाय भगवान विष्णु की भक्ती करता था। 

# # इसी वजह से हिरण्यकशयप ने होलिका को प्रह्लाद को अपनी गोद में लेकर आग में बैठने को कहा जिसमें भक्त प्रह्लाद तो बच गये लेकिन होलिका मारी गई।जबकि, उसकी ये योजना भी असफल हो गई, क्योंकि वो भगवान विष्णु का भक्त था इसलिये प्रभु ने उसकी रक्षा की। 

# # षड़यंत्र में होलिका की मृत्यु हुई और प्रह्लाद बच गया।

# # """

# stop = open('static/assets/files/stopwords.txt', encoding="utf8")
# # print(stop)
# stopwords = []
# for x in stop:
#     stopwords.append(x)

# def createfrequencytable(text_string) -> dict:
#     stopWords = set(stopwords)
#     words = word_tokenize(text_string)
#     ps = PorterStemmer()

#     freqTable = dict()
#     for word in words:
#         word=str(word)
#         word = ps.stem(word)
#         if word in stopWords:
#             continue
#         if word in freqTable:
#             freqTable[word] += 1
#         else:
#             freqTable[word] = 1
#     return freqTable

# # print(stopwords)


# def hi_summary(text):

#     ft = createfrequencytable(text)
#     # print(ft)

#     sentences = sent_tokenize(text) # NLTK function
#     # total_documents = len(sentences)
#     # print(sentences)

#     return sentences[0]
#     # print(total_documents)
