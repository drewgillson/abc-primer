import nltk
from nltk import FreqDist, sent_tokenize, word_tokenize
from nltk.corpus import brown
import ssl
import re
import numpy as np

sentence_corpus = " ".join(brown.words())

def getWords(min_len):
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context

    nltk.download('brown')
    nltk.download('punkt')

    source = FreqDist(i.lower() for i in brown.words())
    source = np.array(source.most_common()[:4000])[:,:1]

    # the Brown corpus contains duplicates and contains
    # words with weird punctuation and digits
    word_list = np.unique(np.char.lower(source))
    p = np.random.permutation(word_list.shape[0])
    word_list = word_list[p]

    words = [word for word in word_list if len(word) == len(set(word)) and re.search("[^A-Za-z\ ]", word) == None]

    output = [word for word in words if len(word) >= min_len and len(word) <= (min_len + 1) and word[-1:] != 's']
    return output

def getSentence(word):
    global sentence_corpus

    sentence = [i for i in sent_tokenize(sentence_corpus) if word in word_tokenize(i)]
    sentence.sort(key=len)
    if len(sentence) > 0:
        return sentence[0]
    else:
        return ''

def getWordToSpell(words):
    word_to_spell = words.pop()
    sentence = getSentence(word_to_spell)
    if sentence == '' or word_to_spell == '':
        getWordToSpell(words)
    else:
        print('Can you spell ' + word_to_spell + '?')
        return (word_to_spell, sentence)