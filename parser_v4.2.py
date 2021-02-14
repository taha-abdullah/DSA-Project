from bs4 import BeautifulSoup as bs
# import nltk
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
import os
import sqlite3


# import store.py
# nltk.download('averaged_perceptron_tagger')
# nltk.download('wordnet')
# nltk.download('wordpunct_tokenize')
# nltk.download('stopwords')
# nltk.download('punkt')


# connect to the database
def store_address(doc_id, address):
    conn = sqlite3.connect("forward.db")

    # cursor to move around the database
    c = conn.cursor()

    sql = "INSERT INTO 'forward' (doc_id, address) VALUES( ?, ?)"
    c.execute(sql, (doc_id, address,))
    conn.commit()


def store_words(doc_id, word_list):
    conn = sqlite3.connect("forward.db")

    c = conn.cursor()
    for i_ in range(0, len(word_list), 1):
        sql = "INSERT INTO 'words' (doc_id, word, frequency) VALUES( ?, ?, ?)"
        c.execute(sql, (doc_id, word_list[i_][0], word_list[i_][1],))
        conn.commit()


def reverse(m_unique):
    conn = sqlite3.connect("forward.db")

    c = conn.cursor()
    for i in range(0, len(m_unique), 1):
        sql = "SELECT doc_id FROM words WHERE word LIKE ?"
        doc = c.execute(sql, (m_unique[i],))
        sql_2 = "SELECT frequency FROM words WHERE word LIKE ?"
        freq = c.execute(sql_2, (m_unique[i],))
        sql_3 = "INSERT INTO reverse (word, doc_id, frequency)"
        c.execute(sql_3, (m_unique[i], doc, freq))
        conn.commit()



stop_words = set(stopwords.words('english'))  # sets stopwords

file = r"C:\Users\Taha Abdullah\Desktop\art"

doc_id = 0

# forward = {'doc': doc_id, 'word_list': for_index}
master_unique = []

for root, dirnames, filenames in os.walk(file):
    for filename in filenames:
        if filename.endswith('.html'):
            fname = os.path.join(root, filename)
            with open(fname, encoding='utf-8') as handle:

                doc_id += 1

                # opens file
                # file = open(r"Saturn.html", encoding="utf8")

                soup = bs(handle, 'html.parser')  # makes soup

                # allows for only text
                for script in soup(["script", "style", "link", "meta"]):
                    script.decompose()

                sentence = soup.get_text()  # parses soup
                sentence = sentence.lower()

                tokenizer = RegexpTokenizer(r'\w+')  # sets punctuation
                tokens = tokenizer.tokenize(sentence)  # separates string into list of words and removes punctuation

                filtered_sentence = []
                # lemmatized_list = []

                wnl = WordNetLemmatizer()

                # removes stopwords
                y = pos_tag(tokens)
                # lemmatized_list.append(y)

                for word, tag in pos_tag(tokens):
                    if word not in stop_words:
                        wntag = tag[0].lower()
                        if word.isdigit():
                            continue
                        wntag = wntag if wntag in ['a', 'r', 'n', 'v'] else None
                        lemma = wnl.lemmatize(word, wntag) if wntag else word
                        filtered_sentence.append(lemma)
                    # print(filtered_sentence)

                unique = []
                forwardI = [[]]
                for i in range(0, len(filtered_sentence), 1):
                    cou = 0
                    if filtered_sentence[i] in unique:
                        continue
                    else:
                        unique.append(filtered_sentence[i])
                        for j in range(0, len(filtered_sentence), 1):
                            if filtered_sentence[i] == filtered_sentence[j]:
                                cou += 1
                        forwardI.append([filtered_sentence[i], cou])

                forwardI = forwardI[1:]
                # print(forwardI)

                store_words(doc_id, forwardI)
                store_address(doc_id, fname)

        word_id = 0
        for i in range(0, len(unique), 1):
            if unique[0] not in master_unique:
                master_unique.append(unique[i])
                print("working")

print(master_unique)
reverse(master_unique)
print("done")
"""seen = []
                for_index = [[]]
                for word in filtered_sentence:
                    # print(word)
                    count = 0
                    for word2 in filtered_sentence:
                        if word == word2:
                            count += 1
                        if word not in seen:
                            for_index.append([word, count])
                            seen.append(word)
                    seen = []


                for_index = for_index[1:]

                print(for_index)

                # store_address(doc_id, fname)
                # store_words(doc_id, for_index)



                    # print(for_index)

                    # forward['doc'] = doc_id
                    # forward['word_list'] = for_index"""
