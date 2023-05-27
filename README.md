# Bilingual Grammar Error Correction Tool using Deep Learning (English and Hindi)

## Introduction

43.63 percent of the Indian population speak Hindi. Over 42 percent of children in the country study in Hindi-medium schools. Most of the government’s official websites are bilingual (Hindi and English) and the government is constantly promoting the use of Hindi for official work in banks, public sector undertakings, embassies, and other government offices in India as well as foreign countries. Although there are many English Grammar Error Correction tools readily available, there is hardly any free and efficient Hindi Grammar Error Correction tool that will help both native as well as nonnative Hindi speakers.
Our solution is to develop an efficient grammar error correction tool for English and Hindi languages in the Education domain for the use of students and research personnels which will address this problem. The user will be provided with multiple input options such as file upload, type-in text and speech-to-text. The tool will have features like spellcheck, grammar check, and text summarizer. The users can also opt for the ‘Expert Review’ option which will have additional features like cross checking the corrected document and Chat with an expert. A user can get registered as an Expert by uploading their language certification proof which will be validated for the expert’s approval.

## Motivation

As one of the most widely used languages in the world, English plays a vital role in communication with the world. In fact, India ranks second in the countries with the most English speakers worldwide. However, English is mostly spoken as a second language in India. 
The percentage of Hindi-speaking population in India is the largest and it is only growing over the years. The Indian government is constantly promoting the use of Hindi for official work in banks, public sector undertakings, embassies, and other government offices in India as well as in foreign countries. According to the policy by the Ministry of Home Affairs (MHA), all the government websites are bilingual now - Hindi and English. This has created a demand for grammar and error correction (GEC) tools among people in different sectors like education, corporate, and government institutions. 
Although there are wide options for English GEC tools available, most of them provide limited features in the free version. There are very few efficient and reliable Hindi GEC tools. This has motivated us to build a software which would be a bilingual grammar error correction tool with an additional expert vetting feature that would further increase the efficiency of our system.


## Scope

The objective of the project is to develop an efficient Bilingual Grammar Error Correction (GEC) tool for Hindi and English languages. It will be primarily used by students and teachers in schools, colleges, and academic institutions. This instrument will change the field of education and be a blessing for academics, especially those who speak Hindi. The users will be able to summarize texts and check spelling as well as grammar for the input provided. There are numerous input alternatives available such as speech-to-text, file upload, and text entry. The "Expert Review” option, which has extra features including cross-checking the rectified content and chatting with a verified language expert, is available to premium users. In addition to using the tool as a regular user, the user can register as an expert by uploading documentation of their language qualification, which will be verified before the expert’s acceptance.

## Implementation

### English Grammar Checker

We fine-tune the T5 transformer model from Google for our use case. The T5 model unifies the treatment of many-to-many and many-to-one NLP tasks by encoding each task as a text instruction in the input stream. This makes it possible to train and monitor a single model on a wide range of NLP tasks, including regression, Q&A, classification, summarization, and translation. It is trained on large and diverse datasets as opposed to small ones. The text-to-text method employed in the T5 model works best with the encoder-decoder based transformer architecture. By sharing them between the encoder and decoder, the parameter count can be kept constant without experiencing a significant performance hit, similar to an encoder-only architecture like BERT. We use the public C4 200 M dataset as our corpus for training the model. A subset of this data 125,000 sentence pairs are taken out to be used as the development data for training and the remaining is used for testing. The model was trained in batches of 16 with a learning rate of 2e-5. The weights were stored after every 1000 steps and the best model was saved after training. The model was trained for two epochs on Tesla K80 GPU on Google Colab. Due to computational limits, we could not train for more epochs.

### Hindi Grammar Checker

The Multilingual T5 [20] transformer model was fine-tuned and used it in the Hindi grammar-checking module. The Multilingual T5 model is a pre-trained text to-text transformer model which is trained in a similar way like T5 model. The T5 model is used to solve various tasks like language modeling, text summarization, classification, and translation when the proper model is trained on the proper problems. The Multilingual T5 model is pre-trained on the mC4 corpus, covering 101 languages which also includes Hindi. The model was trained in batches of 20 with a learning rate of 2e-4. The weights were stored after every 2000 steps and the best model was saved after training. We use the Wikiextract dataset as our corpus for training the model. A subset of this data 100,000 sentence pairs is taken out to be used as the development data. This data was split into training and testing. The model was trained in batches of 10 with a learning rate of 5e-4. The weights were stored after every 5000 steps and the best model was saved after training. The model was trained for one epoch on Tesla K80 GPU on Google Colab. 

### English Spell Checker

SymSpell library from Python is used to implement spell correction. The Symmetric Delete spelling correction algorithm simplifies the process of edit candidate generation and dictionary lookup for a given DamerauLevenshtein distance. It is six orders of magnitude faster (than the standard approach with deletes + transposes + replaces + inserts) and language independent. Unlike previous methods, only deletions are required; replacements, additions, and transpositions are not. The dictionary term is deleted when the input term is transposed, replaced, and added to. The speed of the algorithm is a result of the pre-calculation and the low-cost production of delete-only edit candidates. Within a maximum edit distance of 3, an average 5-letter word contains about 3 million potential spelling mistakes, but SymSpell only needs to produce 25 deletes to account for them all, both during pre-calculation and during lookup time. The library offers word segmentation of noisy text, compound aware multi-word spelling correction, and single-word spelling correction.

### Hindi Spell Checker

Hindi spell correction uses the Hunspell library from Python. Hunspell is a spell-checker library that makes use of a special dictionary format containing characters, words, and conjugations which are valid in a certain language. This library extracts the words which have to be spellchecked and parses the document. This is followed by the analysis of each word by breaking it down into its root and conjugation affix. It, then, checks the dictionary for the root and conjugation affix combination. If the combination is invalid in that specific language, corrections are suggested based on similar correct words in the dictionary. For suggestion, Hunspell tries a number of various combinations of the incorrect word to see if any new words are produced and also compares the resemblance of misspelled words to all dictionary stems, then searches for forms with affixes that are most similar to those stems. 

### English Text Summarizer

We use the extractive technique for our text summarizer part of the GEC Tool. The summarization feature uses the LexRank library of the Sumy package in Python. Sumy package is an automatic text summarization library using unsupervised graph based approach. The measure of similarity of sentences is calculated by finding the TF-IDF vector of each sentence. TF stands for term frequency, which is based on the total number of occurrences of a particular term in the sentence and IDF stands for inverse document frequency which is the logarithmic division of the total number of sentences (N) and the number of sentences the particular term occurs in. The cosine similarity of the tfidf vectors is found using the following equation: where, tf is number of occurrences of words in a sentence. Each sentences in the cluster formed is assessed using eigen vector centrality based on its lexical properties. The method to calculate centrality of sentences in a cluster using eigen vectors is given by equation 
1. p T B = p T (1) 
Where matrix B is the adjacency matrix obtained from the similarity graph by dividing each element by the corresponding row sum. pT is the left eigenvector of the matrix B with the corresponding eigenvalue of 1. 

### Hindi Text Summarizer

We make use of the LexRank algorithm to implement Hindi text summarization. It is an algorithm of an unsupervised and extractive text summarization library in Python called Sumy. Since it caters to only the English language, we use Google Translate API with the help of Python’s googletrans library. In the LexRank algorithm, we initially concatenate all the text present in each document and split it into individual sentences. This is followed by finding the vector representation (word embeddings) for every particular sentence using punkt tokenizer and CountVectorizer modules of the nltk package. We then calculate the similarity between the sentence vectors stored in the form of a matrix, which is then converted and represented as a graph using the Networkx library, with sentences as its vertices and similarity scores as edges, for the sentence rank calculation. Lastly, the sentences which are ranked at the top are selected to form the final summary. 

### Expert Vetting

The output produced by the GEC Tool may or may not be accurate according to the user's demands and expectations. Hence, Fig. 3. TextRank Algorithm, a feature to get the results generated reviewed by a human expert user, is also incorporated in the application. This expert is registered in the system as a separate category of user, whose credentials are verified before assignment of the expert role. The expert can register themselves for either Hindi or English or both languages at once. The user has the liberty to opt for this feature in order to get the results manually verified, to make the certain required changes and to reproduce the finalized documentation according to user specific guidelines. The expert allocation is done randomly to each general user who chooses the expert vetting feature, and the user can chat and convey their requirements to the expert by the help of an anonymous chat feature as a means of secure communication between them.

## Future Work

The GEC tool only supports English and Hindi currently. More international, regional, or local languages will be introduced in the future, depending on the usage location. The programme will contain paraphrasing and a plagiarism checker, both of which are widely utilized in many different businesses. Regressive testing will be used to evaluate the language model’s fine-tuning process, and it will be applied accordingly.

## Test cases

The accompanying document details all of the test scenarios and also includes a comparison with another online tool.

[Test case document](https://docs.google.com/document/d/1k5p1NYFjGmAx2dSZtgM60r2WVttQBowIZ3-_OvKWqIs/edit?usp=sharing)

## Developers

Made by: 
[@devanshiipatel](https://github.com/devanshiipatel) 
[@sreevidya-m](https://github.com/sreevidya-m) 
[@kumaripoonam9](https://github.com/kumaripoonam9) 
[@dishika1606](https://github.com/dishika1606)  

## Instructions to start the project

The folder labelled "djangoapp" contains the actual live code.
After entering the directory where that folder is located, perform the following actions.

1. Create a python virtual enviroment
2. Run the following command

```
pip install -r requirements.txt

python manage.py runserver
```
