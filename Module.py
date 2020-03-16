from langdetect import detect
from nltk import SnowballStemmer, word_tokenize
from nltk.corpus import stopwords
import string
import sys
import wikipedia
import db_conn


# TODO: implements wikipedia module

class ThemeAi:
    tema = ""
    labels = {}

    def __init__(self, theme):
        db_conn.tables_create()
        self.tema = theme

    @staticmethod
    def sentence_stemming(sentence):
        options = {
            "ar": "arabic", "da": "danish", "nl": "dutch", "en": "english", "fi": "finnish", "fr": "french",
            "de": "german", "hu": "hungarian", "it": "italian", "no": "norwegian", "pt": "portuguese", "ro": "romanian",
            "ru": "russian", "es": "spanish", "sw": "swedish"
        }
        c = detect(sentence)
        try:
            stemmer = SnowballStemmer(options[c])
        except KeyError:
            print("Language not supported")
            sys.exit()
        s = "".join(stemmer.stem(i) + " " for i in sentence.split())
        return "".join(s + " " for s in word_tokenize(s) if s not in set(stopwords.words(options[c])))

    def sentence_modulation(self, sentence):
        for i in sentence.split():
            if i.isnumeric() or i == "\n":
                sentence = sentence.replace(i + " ", "")
        return self.sentence_stemming("".join(c for c in sentence if c not in string.punctuation).lower())

    def dictionary_learn(self, sentence):
        sentence = self.sentence_modulation(sentence)
        for i in sentence.split():
            db_conn.upsert_data(self.tema, i, sentence.count(i+" ")/len(sentence.split()))

    def comp_fill(self, sentence):
        sentence = self.sentence_modulation(sentence)
        comparison = {}
        for i in sentence.split():
            comparison[i] = sentence.count(i)
        return comparison

# TODO: reformat comparison

    def comparison(self, sentence):
        comparison = self.comp_fill(sentence)
