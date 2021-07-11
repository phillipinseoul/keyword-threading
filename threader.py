from logging import lastResort
from posix import EX_NOPERM
from typing import Type
from pororo import Pororo
from krwordrank.word import summarize_with_keywords
import os
from khaiii import KhaiiiApi

# Initialize khaiii object
khaiiiWord = KhaiiiApi()

### Get .txt files from directory /textfiles
os.chdir('meeting_example')
ex_text = []
list_of_files = sorted(os.listdir())
for f in list_of_files:
    with open(f) as text_file:
        text_data = text_file.read().replace("\n", " ")
        text_file.close()
        ex_text.append(text_data)

### Define functions for keyword threading
compare_keylist = Pororo(task="zero-topic", lang="ko")
textNum = 1

class TextClass:
    def __init__(self, text):
        self.keywords = []
        self.text = text
    def add_keyword(self, key):
        self.keywords.append(key)

# Preprocessing: Extract nouns in a text
def preprocessing(newText):
    original_text = newText.text
    sentences = original_text.replace("\n", "").replace('?', '.').replace('!', '.').split('. ')
    processed_text = ''
    for sentence in sentences:
        word_analysis = khaiiiWord.analyze(sentence)
        temp = []
        for word in word_analysis:
            for morph in word.morphs:
                if morph.tag in ['NNP', 'NNG'] and len(morph.lex) > 1:
                    temp.append(morph.lex)
        temp = ' '.join(temp)
        temp += '. '
        processed_text += temp
    return processed_text

def updateLatestText(processedText, latestText):
    if len(latestText) == 6:
        latestText.pop(0)
    latestText.append(processedText)
    return latestText

def keyword_extractor(newText, textList, latestText):
    processedText = preprocessing(newText)
    sentences = processedText.split('. ')
    try:
        keywords = summarize_with_keywords(sentences, min_count=1, max_length=15)
        for word, r in sorted(keywords.items(), key=lambda x:x[1], reverse=True)[:3]:
            # print("%s: %.4f" % (word, r))
            if r >= 1.5:
                newText.add_keyword(word)
        textList.append(newText)
        latestText = updateLatestText(processedText, latestText)
        return newText, textList, latestText
    except AttributeError:
        print("Attribute Error 발생")
        

def get_trending_keyword(latestText):
    sentences = []
    for text in latestText:
        sentences += text.split('.')
    sentences = list(filter(None, sentences))

    trending_keywords = []
    keywords = summarize_with_keywords(sentences, min_count=1, max_length=15)
    i = 1
    for word, r in sorted(keywords.items(), key=lambda x:x[1], reverse=True)[:10]:
        trending_keywords.append(word)
        print("%d.\t%s" % (i, word))
        i += 1
    return trending_keywords

### Get input for default keyword list
if __name__ == "__main__":
    textList = []           # List of all texts
    latestText = []         # List of latest 6 'processed' text
    tNum = 0
    for text in ex_text:
        newText = TextClass(text)
        newText, textList, latestText = keyword_extractor(newText, textList, latestText)
        tNum += 1
        print("Text%d: " % tNum + text[:50] + "...", end="\t")
        for keyword in newText.keywords:
            print("#%s " % keyword, end="")
        print()

        if tNum % 3 == 1 or tNum % 3 == 2 or tNum == 3:
            continue
        else:
            trending = get_trending_keyword(latestText)
            print('\n\n[Trending Keywords]')
            n = 1
            for word in trending:
                print("%d.\t%s" % (n, word))
                n += 1
            print()