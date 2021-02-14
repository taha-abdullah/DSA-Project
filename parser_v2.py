from bs4 import BeautifulSoup as bs
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
import os

# nltk.download('averaged_perceptron_tagger')
# nltk.download('wordnet')
# nltk.download('wordpunct_tokenize')
# nltk.download('stopwords')
# nltk.download('punkt')


stop_words = set(stopwords.words('english'))  # sets stopwords

file = r"\Users\Taha Abdullah\Desktop\articles"

doc_id = 0
for_index = [[]]

forward = {'doc': doc_id, 'word_list': for_index}

for root, dirnames, filenames in os.walk(file):
    for filename in filenames:
        if filename.endswith('.html'):
            fname = os.path.join(root, filename)
            # print('Filename: {}'.format(fname))
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

                tokenizer = RegexpTokenizer(r'\w+')  # sets punctuation
                tokens = tokenizer.tokenize(sentence)  # separates string into list of words and removes punctuation

                filtered_sentence = []
                # lemmatized_list = []

                wnl = WordNetLemmatizer()

                # removes stopwords
                y = pos_tag(tokens)
                # lemmatized_list.append(y)

                for word, tag in pos_tag(tokens):
                    wntag = tag[0].lower()
                    if word.isdigit():
                        continue
                    wntag = wntag if wntag in ['a', 'r', 'n', 'v'] else None
                    lemma = wnl.lemmatize(word, wntag) if wntag else word
                    filtered_sentence.append(lemma)

                seen = set()
                for word in filtered_sentence:
                    count = 0
                    for word2 in filtered_sentence:
                        if word == word2:
                            count += 1
                    if word not in seen:
                        for_index.append([word, count])
                        seen.add(word)

                    forward['doc'] = doc_id
                    forward['word_list'] = for_index

                print(forward)
