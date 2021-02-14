from bs4 import BeautifulSoup as bs
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer

# nltk.download('averaged_perceptron_tagger')
# nltk.download('wordnet')
# nltk.download('wordpunct_tokenize')
# nltk.download('stopwords')
# nltk.download('punkt')


stop_words = set(stopwords.words('english'))  # sets stopwords

# opens file
file = open(
    "/Users/Taha/PycharmProjects/DSAproject_v_0.1/Violin - Simple English Wikipedia, the free encyclopedia.html")

soup = bs(file, 'html.parser')  # makes soup

# allows for only text
for script in soup(["script", "style"]):
    script.extract()

sentence = soup.get_text()  # parses soup

tokenizer = RegexpTokenizer(r'\w+') # sets punctuation
tokens = tokenizer.tokenize(sentence)  # separates string into list of words and removes punctuation

filtered_sentence = []
lemmatized_list = []

wnl = WordNetLemmatizer()


# removes stopwords
y = pos_tag(tokens)
lemmatized_list.append(y)

for w in lemmatized_list:
    if w[0] not in stop_words:
        w = wnl.lemmatize(w[0], pos=w[1])
        filtered_sentence.append(w)

print(lemmatized_list)
print(tokens)
print(filtered_sentence)