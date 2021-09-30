###implementing multivariate model
import string
import nltk
from nltk.corpus import stopwords
import pandas as pd
import numpy as np
import re
import time
start=time.time()
print("--------Maltivariate Model----------\n")
####importing data set
document_data= pd.read_csv('C:/Users/com/Desktop/traindata.txt',sep='\t',names=['Category','data'])
train_data = document_data.iloc[:,:]
train_data['data']=train_data['data'].str.lower()
#preprocessing of training data set
def text_cleaning(d):
    remove_puct=[char for char in d if char not in string.punctuation]
    remove_puct=''.join(remove_puct)
    #print(remove_puct)
    return [word for word in remove_puct.split() if word.lower() not in stopwords.words('english')]
train_data['data']=train_data['data'].apply(text_cleaning)

###creating vocabalary 
vocabalary = []
for d in train_data['data']:
    for word in d:
        vocabalary.append(word)
        
vocabalary = list(set(vocabalary))
print("vocabalary :\n")
print(vocabalary)
word_counts_per_data = {unique_word: [0] * len(train_data['data']) for unique_word in vocabalary}

for i, d in enumerate(train_data['data']):
    for word in d:
        word_counts_per_data[word][i] += 1
        
word_count = pd.DataFrame(word_counts_per_data)

train_clean_data = pd.concat([train_data, word_count], axis=1)

CV = train_clean_data[train_clean_data['Category'] == 'CV']
DL = train_clean_data[train_clean_data['Category'] == 'DL']
#####calculating probability of given class DL and CV
prob_cv = len(CV) / len(train_clean_data)
prob_dl = len(DL) / len(train_clean_data)
print("\nprobability of CV class: {}".format(prob_cv))
print("probability of DL class: {}\n".format(prob_dl))
num_words_per_cv_message = CV['data'].apply(len)
num_cv = num_words_per_cv_message.sum()

num_words_per_dl_message = DL['data'].apply(len)
num_dl = num_words_per_dl_message.sum()

vocab_len = len(vocabalary)

###assuming smoothing factor 
alpha= 1

prob_list_cv = {u_word:0 for u_word in vocabalary}
prob_list_dl = {u_word:0 for u_word in vocabalary}

###calculating probability of each word of train data with respective class
for word in vocabalary:
    num_word_given_cv = CV[word].sum()
    prob_word_given_cv = (num_word_given_cv + alpha) / (num_cv + 2)
    prob_list_cv[word] = prob_word_given_cv

    num_word_given_dl = DL[word].sum() 
    prob_word_given_dl = (num_word_given_dl + alpha) / (num_dl + 2)
    prob_list_dl[word] = prob_word_given_dl
    

######defination for prediction of class of new document
def predict_class(D4):

    
    D4 = D4.lower()
    D4=text_cleaning(D4)
    p1=prob_cv
    p2=prob_dl
    for word in vocabalary:
        if word in D4:
            p1 *= prob_list_cv[word]
            p2 *= prob_list_dl[word]
        else: 
            p1 *= 1-prob_list_cv[word]
            p2 *= 1-prob_list_dl[word]

   ###comparing probability of class CV and DL with respective test data
    print("p(CV|D4): {}".format(p1))
    print("p(DL|D4): {}\n".format(p2))
    
    print("Class of test document is :\n")
    if p1 > p2:
        print('CV')
        
    elif p1 < p2:
        print('DL')
            
###passing test document
predict_class('Deep learning based computer vision methods have been used for facial recognition.')
end=time.time()
print("\nTime taken :",end-start)