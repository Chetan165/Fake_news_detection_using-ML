# -*- coding: utf-8 -*-
import pickle
import pandas as pd
import numpy as np
import re  #regular expression lib
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import xgboost as xgb
from sklearn.metrics import accuracy_score
import streamlit as st

import nltk
nltk.download('stopwords')

port_stem=PorterStemmer()
def stemming(text):
   stemmed_text=re.sub('[^a-zA-Z]',' ',text) #replaces all the characters not belonging in set(a-z,A-Z) like 1,2,@,! etc by ' '
   stemmed_text=stemmed_text.lower() #converting to lower alphabets
   stemmed_text=stemmed_text.split() #splitting each word to list
   stemmed_text=[port_stem.stem(word) for word in stemmed_text if not word in stopwords.words('english')] #stems each word which is not present in stopwords
   stemmed_text=' '.join(stemmed_text)
   return stemmed_text  

model=pickle.load(open("model1.pkl", 'rb'))
model2=pickle.load(open("model2.pkl", 'rb'))
model3=pickle.load(open("model_nb.pkl", 'rb'))
vectorizer= pickle.load(open("vectorizer_2.pkl", "rb"))



def manual(user_input):
  data={'text':[user_input]}
  df=pd.DataFrame(data)
  df['text']=df['text'].apply(stemming)
  new_df=df['text']
  new_df=vectorizer.transform(new_df)
  fianl_predictions=[model.predict(new_df),model2.predict(new_df),model3.predict(new_df)]
  if (fianl_predictions.count(0)>=2):
     return 0
  else:
     return 1
    
  

def main():
  import streamlit as st
  st.set_page_config(page_title="The Truth Matrix", page_icon="🔍", layout="wide")
  st.title("📰 Welcome to The Truth Matrix")
  st.markdown("""
  ### 🔍 How Does This Work?
  Our **Fake News Detection Tool** combines advanced **Machine Learning** models and **Natural Language Processing** techniques to accurately identify fake news.

  Here's how it works:
   - 🧠 We analyze the news headline or article you provide.
   - ⚙️ The text is transformed into features using the **TF-IDF Vectorizer**.
   - 🛠️ The features are processed by **Logistic Regression**, **XGBoost**, and **Naive Bayes** models.
   - 🔗 These models work together using **Majority Voting** to give you the final prediction.

   Whether it's **Indian news** or **global updates**, our ensemble model is fine-tuned to spot potential misinformation with **high accuracy**. Paste your article below, and in seconds, you'll know if it's likely **real or fake**!
   """)
  st.markdown("""
  ### 📝 Paste Your News Article Below:
  Get an instant prediction on whether it's fake or real!
  """)
  user_input = st.text_input('Paste the article:')
  prediction=''
  if st.button("click to know truth "):
     ans=manual(user_input)
     if(ans==0):
       prediction="news is REAL"
     else:
       prediction="news might be FAKE"
  st.success(prediction)
if __name__=='__main__':
   main()
