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

try:
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

    train, test = train_test_split(df, test_size=0.8, random_state=42)

    #Feature Extraction
    cv = CountVectorizer()
    X_train = cv.fit_transform(train.text)
    X_test = cv.transform(test.text)

    #model
    model = MultinomialNB()
    model.fit(X_train, train.score_sentiment)
    y_pred = model.predict(X_test)
    y_pred = y_pred.astype(np.int16)

    st.text('Model Report :\n'+classification_report(test.score_sentiment,y_pred,target_names=['positif','netral','negatif'],labels=[0,1,2]))
    st.write('Data Testing : ',len(test),'%')
    st.write('Data Training : ',len(train),'%')
    st.write('Accuracy : ',accuracy_score(test.score_sentiment,y_pred))
    st.write('F1 Score : ',f1_score(test.score_sentiment.astype(np.int16), y_pred, average='macro'))
    st.write('Precision : ',precision_score(test.score_sentiment, y_pred, average='macro'))
    st.write('Recall : ',recall_score(test.score_sentiment, y_pred, average='macro'))
except:
    print("error")