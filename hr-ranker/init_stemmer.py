from pymystem3 import Mystem
from nltk.stem.snowball import SnowballStemmer
from stop_words import get_stop_words

if __name__ == '__main__':
    MYSTEM = Mystem()
    STEMMER = SnowballStemmer("russian")
    STOP_WORDS = list(get_stop_words("russian"))