import warnings
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score,f1_score, recall_score, precision_score, classification_report

warnings.filterwarnings('ignore')
df = pd.read_csv('../data_tw.csv')
df

def analyze(score):
    if score == "positif" :
        return 1
    elif score == "netral" :
        return 0
    else:
        return -1

df['score_sentiment'] = df['sentimen'].apply(analyze)
df

train, test = train_test_split(df, test_size=0.2, random_state=30)

#Feature Extraction
cv = CountVectorizer()
X_train = cv.fit_transform(train.text)
X_test = cv.transform(test.text)

#model
model = MultinomialNB()
model.fit(X_train, train.score_sentiment)
y_pred = model.predict(X_test)
y_pred = y_pred.astype(np.int16)

def acc():
    print(classification_report(test.score_sentiment,y_pred,target_names=['positif 1','netral 0','negatif -1'],labels=[0, 1, 2]))
    print("Data Test = ",len(test),'%')
    print("Data Train = ",len(train),'%')
    print("Akurasi = ",accuracy_score(test.score_sentiment,y_pred))
    print("F1 = ",f1_score(test.score_sentiment.astype(np.int16), y_pred, average='macro'))
    print("Precision = ",precision_score(test.score_sentiment, y_pred, average='macro'))
    print("Recall = ",recall_score(test.score_sentiment, y_pred, average='macro'))