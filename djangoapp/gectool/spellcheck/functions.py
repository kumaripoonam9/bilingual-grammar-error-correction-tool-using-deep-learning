import PyPDF2
import docx


def handle_uploaded_file(f):
    ext = f.name.split('.')[-1]
    with open('static/upload/file.'+ext, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return ext


# for .txt files
def txtToText(filename):
    with open(filename) as f:
        contents = f.read()
        # result = contents.replace('\n', ' ')
        return contents


# for .docx files
def docxToText(filename):
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    x = '\n'.join(fullText)
    return x


# for .pdf
def pdfToText(filename):
    # creating a pdf file object
    pdfFileObj = open(filename, 'rb')

    # creating a pdf reader object
    pdfReader = PyPDF2.PdfReader(pdfFileObj)

    # printing number of pages in pdf file
    # print(len(pdfReader.pages))

    final_text = []
    for page in range(len(pdfReader.pages)):
        # print(page)
        pageObj = pdfReader.pages[page]
        text = pageObj.extract_text()
        final_text.append(text)
        # pdfFileObj.close()

    result = " ".join(final_text)
    # result = result.replace('\n', '')

    return result

# creating a page object
# pageObj = pdfReader.pages[:7]

# extracting text from page
# print(pageObj.extract_text())

# closing the pdf file object
# pdfFileObj.close()
