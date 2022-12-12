import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer,TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix,classification_report
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

st.sidebar.success("Pilih Halaman Diatas")
st.title("Perhitungan Akurasi")

try:
   file_csv=st.file_uploader("Unggah File CSV")
   df = pd.read_csv(file_csv)
   st.text("Dataset")
   df=df.drop(index=0, axis=0, inplace=False)
   tabel=['Name', 'Comment', 'Time', 'Likes', 'Reply Count','text_clear','polarity_score','sentimen']
   st.write(df.loc[:,tabel])

   def analyze(score):
      if score == "positif" :
         return 1
      elif score == "netral" :
         return 0
      else:
         return -1

   df['score_sentiment'] = df['sentimen'].apply(analyze)

   X=df['Comment']
   y=df['score_sentiment']

   bow_transformer=CountVectorizer()
   X=bow_transformer.fit_transform(df['Comment'].values.astype('U'))

   #TFID Transform
   tf_transform=TfidfTransformer(use_idf=False).fit(X)
   X=tf_transform.transform(X)

   X_train, X_test, y_train,y_test = train_test_split(X,y, test_size=0.3,random_state=0)

   #model
   model = MultinomialNB()
   model.fit(X_train, y_train)
   pred = model.predict(X_test)

   st.write('Confusion Matrix : ',confusion_matrix(y_test,pred))
   f, ax = plt.subplots(figsize=(8,5))
   sns.heatmap(confusion_matrix(y_test,pred), annot=True, fmt=".0f", ax=ax)
   plt.xlabel("y_head")
   plt.ylabel("y_true")
   plt.show()
   st.pyplot(f)

   st.text('Model Report :\n'+classification_report(y_test,pred))
except:
   print("error")