import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Ensure that NLTK downloads are done before using preprocess (we'll instruct how to download).
_stopwords = None
_lemmatizer = None

def ensure_nltk():
    global _stopwords, _lemmatizer
    if _stopwords is None or _lemmatizer is None:
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        nltk.download('wordnet', quiet=True)
        nltk.download('omw-1.4', quiet=True)
        _stopwords = set(stopwords.words('english'))
        _lemmatizer = WordNetLemmatizer()

def preprocess(text: str) -> str:
    """
    Lowercase, remove non-alphanumerics, tokenize, remove stopwords and lemmatize.
    Returns a cleaned single string (space-separated tokens) suitable for TF-IDF.
    """
    ensure_nltk()
    text = text.lower()
    # remove non-alphanumeric characters (keeps spaces)
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    tokens = nltk.word_tokenize(text)
    tokens = [t for t in tokens if t.isalpha() and t not in _stopwords]
    tokens = [_lemmatizer.lemmatize(t) for t in tokens]
    return " ".join(tokens)
