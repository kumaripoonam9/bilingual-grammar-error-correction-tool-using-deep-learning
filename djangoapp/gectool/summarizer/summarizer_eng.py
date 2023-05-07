from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from math import ceil



# sample text

# doc="""OpenGenus Foundation is an open-source non-profit organization with the aim to enable people to work offline for a longer stretch, reduce the time spent on searching by exploiting the fact that almost 90% of the searches are same for every generation and to make programming more accessible.
# OpenGenus is all about positivity and innovation.
# Over 1000 people have contributed to our missions and joined our family. We have been sponsored by three great companies namely Discourse, GitHub and DigitalOcean. We run one of the most popular Internship program and open-source projects and have made a positive impact over people's life.
# """

def eng_summary(text):
    # For Strings
    parser=PlaintextParser.from_string(text,Tokenizer("english"))
    
    length = ceil(len(text.split('.'))*4/10)

    # Using LexRank
    summarizer = LexRankSummarizer()
   
    #Summarize the document with 4 sentences
    summary = summarizer(parser.document, length)
    
    # result = ""
    # for sentence in summary:
        # result += sentence
        
    summary = ' '.join(map(str, summary))
    # summary = " ".join(summary)

    return summary
