from distutils.log import info
import nltk
import string
from nltk.corpus import stopwords
nltk.download('stopwords')
from nltk.stem.porter import PorterStemmer
import re

from nltk.corpus import stopwords

# definir les focntions utilisées pour la préparation du texte :
stopWords = set(stopwords.words('french'))

def preprocessor(text):
    text = text.lower()
    text = re.sub(r"['’']", ' ', text)
    text = ''.join([i for i in text if i in string.ascii_lowercase+' '])
    text = ' '.join([PorterStemmer().stem(word) for word in text.split()])
    text = ' '.join([word for word in text.split() if word not in stopWords])
    return text

def compact(lst):
    return list(filter(None, lst))
        

def flatten(t):
    return [item for sublist in t for item in sublist]


