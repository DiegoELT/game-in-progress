import nltk
import string
import numpy as np

from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from unidecode import unidecode

nltk.data.path.append('nltk_data')

def pre_process(corpus, n = 20):
  corpus = corpus.lower()
  stopset = stopwords.words('english') + list(string.punctuation)
  corpus = [token for token in word_tokenize(corpus) if token not in stopset and len(token) > 3]

  lemmatizer = WordNetLemmatizer()
  for i in range(len(corpus)):
    corpus[i] = lemmatizer.lemmatize(unidecode(corpus[i]))

  if len(corpus) < n:
    n = len(corpus)

  return ' '.join(corpus[:n])

class LanguageComparison:
  def __init__(self, model):
    self.model = model
  
  def get_similarity(self, a, b):
    similarities = []
    a_tokens = a.split()
    b_tokens = b.split()

    for at in a_tokens:
      for bt in b_tokens:
        try:
          score = self.model.similarity(at, bt)
          similarities.append(score)
        except: 
          pass

    if len(similarities) > 0:
      return np.average(similarities)
    return 0

  def get_similarity_average(self, query, strings):
    similarities = []

    for entry in strings:
      similarities.append(self.get_similarity(query, entry))

    if len(similarities) > 0:
      return np.average(similarities)
    return 0
  
  def get_most_similar(self, query, strings, n = 10):
    similarity_scores = []

    for entry in strings:
      similarity_scores.append((entry['info'], self.get_similarity(query, entry['text'])))

    if len(similarity_scores) < n:
      n = len(similarity_scores)

    similarity_scores.sort(key = lambda item: -item[1])
    return similarity_scores[:n]
    
