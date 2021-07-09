from pororo import Pororo
from krwordrank.word import KRWordRank, summarize_with_keywords
import operator
import json
import os


### Get .txt files from directory /textfiles

### Define functions for keyword threading
compare_keylist = Pororo(task="zero-topic", lang="ko")
keyword_list = []
text_list = {}

textNum = 1

class TextClass:
    def __init__(self, text):
        self.keywords = []
        self.text = text

    def add_keyword(self, key):
        self.keywords.append(key)


def keyword_threader(text, keyword_list):
    newText = TextClass(text)
    text_list[textNum] = newText
    textNum += 1

    keyScore = compare_keylist(text, keyword_list)
    maxScore = max(keyScore, key=lambda key: keyScore[key])

    if maxScore >= 60:
        newText = put_in_original_keyword(newText, keyScore)
        print("기존의 키워드에 포함됩니다: ", end="")
        print(newText.keywords)
    else:
        print("새로운 키워드가 추가되었습니다: ", end="")
        print(newText.keywords)
        newText = extract_new_keyword(newText)


def put_in_original_keyword(newText, keyScore):
    for key, value in keyScore.items():
        if value >= 60:
            newText.add_keyword(key)

    return newText

def extract_new_keyword(newText):
    text = newText.text
    sentences = text.split('. ')
    try:
        keywords = summarize_with_keywords(sentences, min_count=1, max_length=15)
        for word, r in sorted(keywords.items(), key=lambda x:x[1], reverse=True)[:3]:
            keyword_list.append(word)
            newText.add_keyword(word)
        return newText
    except AttributeError:
        print("Attribute Error 발생")
    
    




    return




### Get input for default keyword list


