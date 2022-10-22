import warnings
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import metrics 
from sklearn.preprocessing import LabelEncoder 
from sklearn.svm import SVC
from sklearn.metrics import classification_report
from datetime import datetime
import streamlit as st

warnings.filterwarnings('ignore')
st.sidebar.success("Pilih Halaman Diatas")
st.title("Perhitungan Akurasi")

#try:
file_csv=st.file_uploader("Unggah File CSV")
data = pd.read_csv(file_csv)
#remove kolom nomer
st.write(data.iloc[:,1:-1])

label_encoder = LabelEncoder()
#convert tgl ke float
dt = int(data.iloc[:,0].strftime("%Y%m%d%H%M%S"))
#mengubah value diagnosis menjadi 1 dan 0 
data.iloc[:,0] = label_encoder.fit_transform(dt.astype('float64'))

paramater = data.iloc[:,1:-1] 
target = data.iloc[:,0]

x_train, x_test, y_train, y_test = train_test_split(paramater.values, target.values, test_size = 0.2)

# The default kernel adalah gaussian kernel
svc = SVC() 
svc.fit(x_train, y_train) 
prediction = svc.predict(x_test)

st.text('Model Report :\n'+classification_report(y_test, prediction,target_names=['positif','netral','negatif'],labels=[0,1,2]))
st.write("Akurasi : ",metrics.accuracy_score(y_test, prediction))
#except:
   #print("error")