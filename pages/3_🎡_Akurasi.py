import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score,classification_report
import streamlit as st

st.sidebar.success("Pilih Halaman Diatas")
st.title("Perhitungan Akurasi")

#try:
file_csv=st.file_uploader("Unggah File CSV")
#impor CSV ke dataset
df = pd.read_csv(file_csv)

st.write(df.loc[:,["tgl","user","text","polarity_score","sentimen"]])

df=df.astype({'sentimen' : 'category'})
df=df.astype({'text' : 'string'})
tf=TfidfVectorizer()
text_tf=tf.fit_transform(df['text'].astype('U'))

X_train, X_test, y_train, y_test = train_test_split(text_tf,df['sentimen'], test_size = 0.2, random_state=42)
 
clf=MultinomialNB().fit(X_train,y_train)
predicted=clf.predict(X_test)
st.write("Accuracy   : ",accuracy_score(y_test,predicted))
st.write("Precision  : ",precision_score(y_test,predicted,average="micro",pos_label="positif"))
st.write("Recall     : ",recall_score(y_test,predicted,average="micro",pos_label="positif"))
st.write("F1 Score   : ",f1_score(y_test,predicted,average="micro",pos_label="positif"))

st.text(classification_report(y_test,predicted,zero_division=0,target_names=['positif','netral','negatif'],labels=[0,1,2]))
#except:
   #print("error")