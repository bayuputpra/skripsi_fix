import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer,TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score,classification_report,f1_score,precision_score,recall_score
import streamlit as st

st.sidebar.success("Pilih Halaman Diatas")
st.title("Perhitungan Akurasi")

#try:
file_csv=st.file_uploader("Unggah File CSV")
df = pd.read_csv(file_csv)
st.write(df.loc[:,["tgl","user","text","text_clear","polarity_score","sentimen"]])

def analyze(score):
   if score == "positif" :
      return 1
   elif score == "netral" :
      return 0
   else:
      return -1

df['score_sentiment'] = df['sentimen'].apply(analyze)

X=df['text']
y=df['score_sentiment']

bow_transformer=CountVectorizer()
X=bow_transformer.fit_transform(df['text'])

#TFID Transform
tf_transform=TfidfTransformer(use_idf=False).fit(X)
X=tf_transform.transform(X)

X_train, X_test, y_train,y_test = train_test_split(X,y, test_size=0.2,random_state=30)

#model
model = MultinomialNB()
model.fit(X_train, y_train)
pred = model.predict(X_test)

st.write('Accuracy : ',accuracy_score(y_test,pred))
st.write('F1 Score : ',f1_score(y_test.astype(np.int16), pred, average='macro'))
st.write('Precision : ',precision_score(y_test, pred, average='macro'))
st.write('Recall : ',recall_score(y_test, pred, average='macro'))
st.text('Model Report :\n'+classification_report(y_test,pred))
#except:
   #print("error")