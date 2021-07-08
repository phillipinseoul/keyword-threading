from pororo import Pororo
from krwordrank.word import KRWordRank, summarize_with_keywords
import operator
import json
import os

### Get .txt files from directory /textfiles

### Define functions for keyword threading
compare_keylist = Pororo(task="zero-topic", lang="ko")

def keyword_threader(text, keylist):
    keyScore = compare_keylist(text, keylist)
    maxScore = max(keyScore, key=lambda key: keyScore[key])

    if 

    return

### Get input for default keyword list


