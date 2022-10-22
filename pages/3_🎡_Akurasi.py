import pandas as pd
from sklearn import svm
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
import streamlit as st

st.sidebar.success("Pilih Halaman Diatas")
st.title("Perhitungan Akurasi")

#try:
file_csv=st.file_uploader("Unggah File CSV")
#impor CSV ke dataset
df = pd.read_csv(file_csv)

st.write(df.loc[:,["tgl","user","text","polarity_score","sentimen"]])

def analyze(score):
   if score == "positif" :
      return 1
   elif score == "netral" :
      return 0
   else:
      return -1

df['score_sentiment'] = df['sentimen'].apply(analyze)
 
X_train, X_test, y_train, y_test = train_test_split(df, test_size = 0.2)
 
#menggunakan SVM library untuk membuat SVM classifier
classifier = svm.SVC(kernel = 'linear')
 
#memasukkan training data kedalam classifier
classifier.fit(X_train, y_train)
 
#memasukkan testing data ke variabel y_predict
y_predict = classifier.predict(X_test)
 
#menampilkan classification report
st.text(classification_report(y_test, y_predict,target_names=['positif','netral','negatif'],labels=[0,1,2]))
#except:
   #print("error")