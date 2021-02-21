from nltk.corpus import stopwords
import string
from nltk.tokenize import wordpunct_tokenize as tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem import WordNetLemmatizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import wordnet as wn
import PyPDF2
import spacy


def train(fnames):
    docs = []

    for i in range(len(fnames)):
        pdffile = open('./' + fnames[i], 'rb')
        print(pdffile)
        pdfReader = PyPDF2.PdfFileReader(pdffile)
        num_pages = pdfReader.numPages
        count = 0
        texts = " "

        while count < num_pages:
            pageObj = pdfReader.getPage(count)
            count += 1
            texts = texts + pageObj.extractText()

        tx = " ".join(texts.split('\n'))

        docs.append(tx)

    print(docs[len(docs)-1])

    #print(docs)

    nlp_model_annotation = spacy.load('./Dashboard/nlpdesc_model')
    nlp_CV_annotation = spacy.load('./Dashboard/nlpdesc_CV_model')

    documents = []

    for index, d in enumerate(docs):
        if index == len(docs)-1:
            document = nlp_model_annotation(d)
        else:
            document = nlp_CV_annotation(d)

        text = ""

        for ent in document.ents:
            # print(f'{ent.label_.upper():{30}} - {ent.text}')
            text = text + str(ent.text)

        if len(text) <100:
            documents.append(d)
        else:
            documents.append(text)
    # print(documents[len(docs)-1])

    wordnet = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))
    table = str.maketrans('', '', string.punctuation)

    modified_arr = [[wordnet.lemmatize(i.lower()) for i in tokenize(d.translate(table)) if i.lower() not in stop_words] for
                    d in documents]

    #print(modified_arr)

    skip = []
    for d in modified_arr:
        for i in range(len(d)):
            synonyms = []
            for syn in wn.synsets(d[i]):
                for l in syn.lemmas():
                    synonyms.append(l.name())
            # print(synonyms)

            for doc in modified_arr:
                for j in range(len(doc)):
                    if doc[j] not in skip:
                        if (doc[j] != d[i]):
                            if doc[j] in synonyms:
                                doc[j] = d[i]
                                if doc[j] not in skip:
                                    skip.append(doc[j])

    #print(skip)
    #print(modified_arr)

    modified_doc = [' '.join(i) for i in
                    modified_arr]  # this is only to convert our list of lists to list of strings that vectorizer uses.
    tf_idf = TfidfVectorizer().fit_transform(modified_doc)

    #print(tf_idf)

    similarity = []

    length = len(documents) - 1
    for i in range(length + 1):
        cosine = cosine_similarity(tf_idf[length], tf_idf[i])
        similarity.append(cosine)
        print(cosine)

    return similarity

def train_desc(fnames):
    docs = []

    for i in range(len(fnames)):
        pdffile = open('./' + fnames[i], 'rb')
        print(pdffile)
        pdfReader = PyPDF2.PdfFileReader(pdffile)
        num_pages = pdfReader.numPages
        count = 0
        texts = " "

        while count < num_pages:
            pageObj = pdfReader.getPage(count)
            count += 1
            texts = texts + pageObj.extractText()

        tx = " ".join(texts.split('\n'))

        docs.append(tx)

    # print(docs[len(docs)-1])

    #print(docs)

    nlp_model_annotation = spacy.load('./Dashboard/nlpdesc_model')
    nlp_CV_annotation = spacy.load('./Dashboard/nlpdesc_CV_model')

    documents = []

    for index, d in enumerate(docs):
        if index == len(docs)-1:
            document = nlp_CV_annotation(d)
        else:
            document = nlp_model_annotation(d)

        text = ""

        for ent in document.ents:
            # print(f'{ent.label_.upper():{30}} - {ent.text}')
            text = text + str(ent.text)

        if len(text) <100:
            documents.append(d)
        else:
            documents.append(text)
    # print(documents[len(docs)-1])

    wordnet = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))
    table = str.maketrans('', '', string.punctuation)

    modified_arr = [[wordnet.lemmatize(i.lower()) for i in tokenize(d.translate(table)) if i.lower() not in stop_words] for
                    d in documents]

    #print(modified_arr)

    skip = []
    for d in modified_arr:
        for i in range(len(d)):
            synonyms = []
            for syn in wn.synsets(d[i]):
                for l in syn.lemmas():
                    synonyms.append(l.name())
            # print(synonyms)

            for doc in modified_arr:
                for j in range(len(doc)):
                    if doc[j] not in skip:
                        if (doc[j] != d[i]):
                            if doc[j] in synonyms:
                                doc[j] = d[i]
                                if doc[j] not in skip:
                                    skip.append(doc[j])

    #print(skip)
    #print(modified_arr)

    modified_doc = [' '.join(i) for i in
                    modified_arr]  # this is only to convert our list of lists to list of strings that vectorizer uses.
    tf_idf = TfidfVectorizer().fit_transform(modified_doc)

    #print(tf_idf)

    similarity = []

    length = len(documents) - 1
    for i in range(length + 1):
        cosine = cosine_similarity(tf_idf[length], tf_idf[i])
        similarity.append(cosine)
        print(cosine)

    return similarity
