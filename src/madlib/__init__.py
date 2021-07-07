import pkg_resources
import json
import gzip
import re

from random import randrange

DICTIONARY = json.loads(gzip.decompress(pkg_resources.resource_string(__name__, 'data/dictionary.json.gz')))
SENTENCES = json.loads(gzip.decompress(pkg_resources.resource_string(__name__, 'data/sentences.json.gz')))


def get_madlib():
    sentence = SENTENCES[randrange(len(SENTENCES))]

    # Sometimes there is punctuation that split won't handle
    sentence = sentence.replace('[[', ' [[').replace(']]', ']] ')
    words = sentence.split()
    for i, word in enumerate(words):
        if word[:2] == '[[' and word[-2:] == ']]':
            type = word[2:-2]
            type_list = DICTIONARY[type]
            word = type_list[randrange(len(type_list))]
            words[i] = word
    return re.sub(r'\s([?.!,:;\'"](?:\s|$))', r'\1', ' '.join(words))
