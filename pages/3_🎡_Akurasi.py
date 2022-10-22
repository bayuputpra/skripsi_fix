import warnings
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score,classification_report,f1_score,precision_score,recall_score
import streamlit as st

warnings.filterwarnings('ignore')
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

X=float(df['text'])
y=df['score_sentiment']

X_train, X_test, y_train,y_test = train_test_split(X,y, test_size=0.2)

#model
model = MultinomialNB()
model.fit(X_train, y_train)
pred = model.predict(X_test)

st.text('Model Report :\n'+classification_report(y_test,pred,target_names=['positif','netral','negatif'],labels=[0,1,2]))
#st.write('Data Testing : ',len(test),'%')
#st.write('Data Training : ',len(train),'%')
st.write('Accuracy : ',accuracy_score(y_test,pred))
#st.write('F1 Score : ',f1_score(test.score_sentiment.astype(np.int16), y_pred, average='macro'))
#st.write('Precision : ',precision_score(test.score_sentiment, y_pred, average='macro'))
#st.write('Recall : ',recall_score(test.score_sentiment, y_pred, average='macro'))
#except:
   #print("error")