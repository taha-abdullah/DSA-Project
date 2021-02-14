from bs4 import BeautifulSoup
import requests
import os
import sys
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
from nltk.stem.porter import *
#nltk.download('punkt')

#with open("beach.html","r",encoding="utf-8") as f:
#    contents = f.read()

#    soup = BeautifulSoup(contents,'lxml')
#    print(soup.h2)
#    print(soup.head)
#file = open(
#"/Users/dell/Downloads/mnb/simple/articles/a/n/d/And.html",encoding = 'utf-8')

file = "/Users/dell/CookiesDownloads/mnb/simple/articles"
for root, dirnames, filenames in os.walk(file):
    for filename in filenames:
        if filename.endswith('.html'):
            fname = os.path.join(root, filename)
            #print('Filename: {}'.format(fname))
            with open(fname,encoding = 'utf-8') as handle:
                soup = BeautifulSoup(handle.read(), 'html.parser')
                for script in soup(["script","style"]):
                    script.extract()
                    sentence = soup.get_text()
                    stop_words = set(stopwords.words('english')) #english stopwords
                    word_tokens = word_tokenize(sentence)
                    filtered_sentence = [w for w in word_tokens if not w in stop_words] 
                      
                    filtered_sentence = [] 

                    #if word is not a stop word, append to filtered sentence list  
                    for w in word_tokens: 
                        if w not in stop_words: 
                            filtered_sentence.append(w)
                    filtered_sentence = [w.lower() for w in filtered_sentence] #convert to lowercase
                    fs = re.sub(r'[^a-zA-Z]',"", str(filtered_sentence)) #remove non alphanumeric

                    stemmer = PorterStemmer()

                    #fs = [stemmer.stem(w) for w in filtered_sentence]

                    print(word_tokens)
                    print(filtered_sentence)
                    print("With alpha numeric characters only")
                    print(fs)
                    print("-----------------------------------------------------------------------")
                    
                                

#indexing

#soup = BeautifulSoup(file, 'html.parser')
#for script in soup(["script","style"]):
#            script.extract()

#print(soup.prettify())








