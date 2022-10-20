import warnings
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

warnings.filterwarnings('ignore')
st.sidebar.success("Pilih Halaman Diatas")
st.title("Perhitungan Akurasi")

#try:
file_csv=st.file_uploader("Unggah File CSV")
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

#split
X_train, X_test, y_train, y_test = train_test_split(df,test_size = 0.2)

vectoriser = TfidfVectorizer(ngram_range=(1,2), max_features=500000)
vectoriser.fit(X_train)

X_train = vectoriser.transform(X_train)
X_test  = vectoriser.transform(X_test)

clf = LogisticRegression()
clf.fit(X_train, y_train)

#classifier dara
nb = MultinomialNB()
#nb = BernoulliNB()
nb.fit(X_train, y_train)
preds = nb.predict(X_test)
st.text(classification_report(y_test, preds))

st.write("Accuracy :", nb.score(X_test, y_test))
#except:
    #print("error")