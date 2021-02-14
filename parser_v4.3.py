from bs4 import BeautifulSoup as bs, ResultSet
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
def forward_table(doc_id, address, header):
    print(header)
    conn = sqlite3.connect("forward.db")

    # cursor to move around the database
    c = conn.cursor()
    sql = "INSERT INTO 'forward' (doc_id, address, heading) VALUES( ?, ?, ?)"
    c.execute(sql, (doc_id, address, header,))
    conn.commit()


def store_words(doc_id, word_list):
    conn = sqlite3.connect("forward.db")

    c = conn.cursor()
    for i_ in range(0, len(word_list), 1):
        sql = "INSERT INTO 'words' (doc_id, word, frequency) VALUES( ?, ?, ?)"
        c.execute(sql, (doc_id, word_list[i_][0], word_list[i_][1],))
        conn.commit()


def get_doc_id(word_):

    conn = sqlite3.connect("forward.db")

    # cursor to move around the database
    c = conn.cursor()

    c.execute("SELECT doc_id FROM words WHERE word = ?", (word_,))
    rows = c.fetchall()
    return rows


def get_frequency(word_, doc_id_):
    conn = sqlite3.connect("forward.db")

    # cursor to move around the database
    c = conn.cursor()

    c.execute("SELECT frequency FROM words WHERE word = ? AND doc_id = ?", (word_, str(doc_id_),))
    rows = c.fetchall()
    return rows


def store_reverse_index(word_id, word, doc_id, frequency):
    conn = sqlite3.connect("forward.db")

    # cursor to move around the database
    c = conn.cursor()

    sql = "INSERT INTO 'reverse' (word_id, word, doc_id, frequency) VALUES( ?, ?, ?, ?)"
    c.execute(sql, (word_id, word, doc_id, frequency,),)
    conn.commit()


stop_words = set(stopwords.words('english'))  # sets stopwords

file = r"C:\Users\Taha Abdullah\PycharmProjects\DSA\articles"

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
                for script in soup(["script", "style"]):
                    script.decompose()

                sentence = soup.get_text()  # parses soup
                sentence = sentence.lower()

                headers = soup.find_all('h1')
                h = [header.get_text() for header in headers]
                if h:
                    h = h[0]
                else:
                    doc_id -= 1
                    continue
                print(h)
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
                forward_table(doc_id, fname, h)

            for i in range(0, len(unique), 1):
                if unique[i] not in master_unique:
                    master_unique.append(unique[i])

print(master_unique)
# REVERSE INDEXER
word_id = 0
for i in master_unique:
    x = get_doc_id(i)
    for j in range(0, len(x), 1):
        x[j] = x[j][0]

    for k in range(0, len(x), 1):
        frequency = get_frequency(i, x[k])
        for m in range(0, len(frequency), 1):
            frequency[m] = frequency[m][0]
        print(frequency)

        store_reverse_index(word_id, i, x[k], frequency[0])
    word_id += 1