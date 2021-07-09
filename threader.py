from posix import EX_NOPERM
from pororo import Pororo
from krwordrank.word import KRWordRank, summarize_with_keywords
import os
from konlpy.tag import Okt

# Initialize Okt object
okt = Okt()

### Get .txt files from directory /textfiles
os.chdir('meeting_example')
ex_text = []
list_of_files = sorted(os.listdir())
for f in list_of_files:
    with open(f) as text_file:
        text_data = text_file.read().replace("\n", " ")
        text_file.close()
        ex_text.append(text_data)

# for f in os.listdir():
#     with open(f) as text_file:
#         text_data = text_file.read().replace("\n", " ")
#         text_file.close()
#         ex_text.append(text_data)

### Define functions for keyword threading
compare_keylist = Pororo(task="zero-topic", lang="ko")
keyword_list = []
text_list = []

textNum = 1

class TextClass:
    def __init__(self, text):
        self.keywords = []
        self.text = text

    def add_keyword(self, key):
        self.keywords.append(key)


def keyword_threader(text, keyword_list):
    newText = TextClass(text)
    text_list.append(newText)

    keyScore = compare_keylist(text, keyword_list)
    maxKey = max(keyScore, key=lambda key: keyScore[key])

    if keyScore[maxKey] >= 70:
        newText = put_in_original_keyword(newText, keyScore)
        print("기존의 키워드에 포함됩니다: ", end="")
        print(newText.keywords)
    else:
        newText = extract_new_keyword(newText)
        print("새로운 키워드가 추가되었습니다: ", end="")
        print(newText.keywords)


def put_in_original_keyword(newText, keyScore):
    for key, value in keyScore.items():
        if value >= 70:
            newText.add_keyword(key)
    return newText

def extract_new_keyword(newText):
    text = newText.text
    sentences = text.split('. ')
    noun_list = okt.nouns(text)         # Get list of nouns in the text

    try:
        keywords = summarize_with_keywords(sentences, min_count=1, max_length=15)
        # Choose top 3 'noun' keywords
        num = 0
        for word, r in sorted(keywords.items(), key=lambda x:x[1], reverse=True):
            if num == 3:
                break
            if word in noun_list:
                keyword_list.append(word)
                newText.add_keyword(word)
                num += 1
        return newText
    except AttributeError:
        print("Attribute Error 발생")

### Get input for default keyword list
if __name__ == "__main__":
    while True:
        input_keyword = input("Default thread를 입력해주세요 (건너뛰기: Enter): ")
        if input_keyword == "":
            break
        else:
            keyword_list.append(input_keyword)
        
    try: 
        if len(keyword_list) == 0:
            raise ValueError
    except ValueError:
        print("키워드를 1개 이상 입력해야 합니다.")

    print("\nDefault Keyword List: ", end="")
    print(keyword_list)
    print()

    stopwords = {}
    j = 1
    for text in ex_text:
        print("Text%d: " % j + text[:50] + "...")
        keyword_threader(text, keyword_list)
        print()
        j += 1
    
    print(keyword_list)

    
