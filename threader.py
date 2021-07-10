from posix import EX_NOPERM
from pororo import Pororo
from krwordrank.word import KRWordRank, summarize_with_keywords
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
# keyword_list = []
# text_list = []

textNum = 1

class TextClass:
    def __init__(self, text):
        self.keywords = []
        self.text = text
    def add_keyword(self, key):
        self.keywords.append(key)

# Returns list of nouns (일반명사, 고유명사) from text
def get_noun_list(text):
    noun_list = []
    noun_analysis = khaiiiWord.analyze(text)
    for word in noun_analysis:
        for morph in word.morphs:
            if morph.tag == 'NNP' or morph.tag == 'NNG':
                noun_list.append(morph.lex)
    return noun_list

def get_trending_keyword(textList):
    allText = ""
    for t in textList:
        allText += (" " + t.text)
    noun_list = get_noun_list(allText)
    sentences = allText.split('. ')
    # Print noun list
    print(noun_list)
    try: 
        keyScore = compare_keylist(allText, noun_list)
        num = 0
        trending_keywords = []
        for word, score in sorted(keyScore.items(), key=lambda x:x[1], reverse=True)[:10]:
            if num == 10:
                break
            # print("%s : %d" % (word, score))
            trending_keywords.append((word, score))
        return trending_keywords
    except ValueError:
        print("Tokens exceeds maximum length: 515 > 512")

### Get input for default keyword list
if __name__ == "__main__":
    text_list = []
    tNum = 0

    for text in ex_text:
        text_list.append(TextClass(text))
        tNum += 1
        print("Text%d: " % tNum + text[:50] + "...")

        if tNum % 2 == 1 or tNum == 2:
            continue
        else:
            tList = text_list[tNum-4 : tNum-1]
            trending = get_trending_keyword(tList)
            for word, score in trending:
                print("%s : %d" % (word, score))
            print()

