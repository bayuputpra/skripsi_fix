from googleapiclient.discovery import build
import pandas as pd
import re
import string
from nltk.tokenize import word_tokenize
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords
import emoji
import streamlit as st

st.sidebar.success("Pilih Halaman Diatas")
hide_st_style="""
        <style>
        #MainMenu {visibility:hidden;}
        </style>
        """
st.markdown(hide_st_style,unsafe_allow_html=True)

api_key = "AIzaSyAdYAdDC85CsvKOhaabOxhiZDKGuDok3vI"
youtube = build('youtube', 'v3', developerKey=api_key)

st.title("Sentimen Analisis Youtube")

try:
    add_selectbox = st.selectbox("Pilih Menu",("pilih salah satu","Cari Dataset", "Hitung Dataset"))
    if add_selectbox=="Cari Dataset":
        searchVid = st.text_input("Masukan Link Video")
        box = [['Name', 'Comment', 'Time', 'Likes', 'Reply Count']]
        data = youtube.commentThreads().list(part='snippet', videoId=searchVid, maxResults='100', textFormat="plainText").execute()
        for i in data["items"]:
            name = i["snippet"]['topLevelComment']["snippet"]["authorDisplayName"]
            comment = i["snippet"]['topLevelComment']["snippet"]["textDisplay"]
            published_at = i["snippet"]['topLevelComment']["snippet"]['publishedAt']
            likes = i["snippet"]['topLevelComment']["snippet"]['likeCount']
            replies = i["snippet"]['totalReplyCount']

            box.append([name, comment, published_at, likes, replies])

        while ("nextPageToken" in data):
            data = youtube.commentThreads().list(part='snippet', videoId=searchVid, pageToken=data["nextPageToken"], maxResults='100', textFormat="plainText").execute()
            for i in data["items"]:
                name = i["snippet"]['topLevelComment']["snippet"]["authorDisplayName"]
                comment = i["snippet"]['topLevelComment']["snippet"]["textDisplay"]
                published_at = i["snippet"]['topLevelComment']["snippet"]['publishedAt']
                likes = i["snippet"]['topLevelComment']["snippet"]['likeCount']
                replies = i["snippet"]['totalReplyCount']

                box.append([name, comment, published_at, likes, replies])

        dataset = pd.DataFrame({'Name': [i[0] for i in box], 'Comment': [i[1] for i in box], 'Time': [i[2] for i in box],
                                'Likes': [i[3] for i in box], 'Reply Count': [i[4] for i in box]})

        def preProcess(text):
            #removing number
            text=text.lower()
            text=re.sub(r"\d+","",text)
            #remove mention,link,hashtag,emoji
            text=" ".join(re.sub("([@#][A-Za-z0-9]+)|(\w+:\/\/\S+)"," ",text).split())
            text = emoji.demojize(text)
            #remove punctuation
            text=text.translate(text.maketrans("","",string.punctuation))
            #remove whitespace
            text=text.strip()
            space=text.split()
            text=word_tokenize(text)
            stop_words = set(stopwords.words('indonesian'))
            text = [word for word in text if not word in stop_words]
            return text

        dataset['text_clear']=dataset['Comment'].apply(preProcess)

        positive=dict()
        import csv
        with open('positive.csv','r')as csvfile:
            reader=csv.reader(csvfile,delimiter=',')
            for row in reader:
                positive[row[0]]=int(row[1])
                        
        negative=dict()
        import csv
        with open('negative.csv','r')as csvfile:
            reader=csv.reader(csvfile,delimiter=',')
            for row in reader:
                negative[row[0]]=int(row[1])

        #function to determine sentiment polarity of tweets
        def sentiment_analysis_indonesia(text):
                #for word in text
                score=0
                for word in text:
                    if(word in positive):
                        score=score+positive[word]
                for word in text:
                    if(word in negative):
                        score=score+negative[word]
                polarity=''
                if (score > 0):
                    polarity = "positif"
                elif (score == 0):
                    polarity = "netral"
                else:
                    polarity = "negatif"
                return score,polarity
                    
        results=dataset['text_clear'].apply(sentiment_analysis_indonesia)
        results=list(zip(*results))
        dataset['polarity_score']=results[0]
        dataset['sentimen']=results[1]

        st.text("Dataset")
        dataset.reset_index()
        st.write(dataset.drop(index=0, axis=1, inplace=False))
        st.download_button(label="Download CSV", data=dataset.to_csv(),mime="text/csv",file_name="data_yt.csv")

        tweet_positif = dataset[dataset["sentimen"]=="positif"]
        tweet_netral = dataset[dataset["sentimen"]=="netral"]
        tweet_negatif = dataset[dataset["sentimen"]=="negatif"]

        st.text("Hasil Sentimen")
        jmlA=len(tweet_positif)
        jmlB=len(tweet_netral)
        jmlC=len(tweet_negatif)
        persenA="{}%".format(100*len(tweet_positif)/len(dataset))
        persenB="{}%".format(100*len(tweet_netral)/len(dataset))
        persenC="{}%".format(100*len(tweet_negatif)/len(dataset))
        df=pd.DataFrame({'sentimen':["positif","netral","negatif"],'jumlah':[jmlA,jmlB,jmlC],'persen':[persenA,persenB,persenC]})
        st.write(df)

        st.text("Pie Chart")
        sentiment_counts = dataset.groupby(["sentimen"]).size()
        fig,ax=plt.subplots()
        sentiment_counts.plot.pie(autopct='%1.1f%%', startangle=270, fontsize=12, label="")
        plt.figure(figsize=(6,6), dpi=100)
        ax.axis('equal')
        st.pyplot(fig)

        st.text("WordCloud")
        def PlotWordcloud():
            stop_words = set(stopwords.words('indonesian'))
            wordcloud = WordCloud(stopwords = stop_words,background_color="white", width=2500, height=2000).generate(str(dataset['Comment']))
            plt.imshow(wordcloud)
            plt.axis("off")
            plt.show()
            st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot(PlotWordcloud())

    elif add_selectbox=="Hitung Dataset":
        file_csv=st.file_uploader("Unggah File CSV")
        dataset = pd.read_csv(file_csv)
        st.text("Dataset")
        dataset=dataset.drop(index=0, axis=0, inplace=False)
        tabel=['Name', 'Comment', 'Time', 'Likes', 'Reply Count','text_clear','polarity_score','sentimen']
        st.write(dataset.loc[:,tabel])

        tweet_positif = dataset[dataset["sentimen"]=="positif"]
        tweet_netral = dataset[dataset["sentimen"]=="netral"]
        tweet_negatif = dataset[dataset["sentimen"]=="negatif"]

        st.text("Hasil Sentimen")
        jmlA=len(tweet_positif)
        jmlB=len(tweet_netral)
        jmlC=len(tweet_negatif)
        persenA="{}%".format(100*len(tweet_positif)/len(dataset))
        persenB="{}%".format(100*len(tweet_netral)/len(dataset))
        persenC="{}%".format(100*len(tweet_negatif)/len(dataset))
        df=pd.DataFrame({'sentimen':["positif","netral","negatif"],'jumlah':[jmlA,jmlB,jmlC],'persen':[persenA,persenB,persenC]})
        st.write(df)

        st.text("Pie Chart")
        sentiment_counts = dataset.groupby(["sentimen"]).size()
        fig,ax=plt.subplots()
        sentiment_counts.plot.pie(autopct='%1.1f%%', startangle=270, fontsize=12, label="")
        plt.figure(figsize=(6,6), dpi=100)
        ax.axis('equal')
        st.pyplot(fig)

        st.text("WordCloud")
        def PlotWordcloud():
            stop_words = set(stopwords.words('indonesian'))
            wordcloud = WordCloud(stopwords = stop_words,background_color="white", width=2500, height=2000).generate(str(dataset['Comment']))
            plt.imshow(wordcloud)
            plt.axis("off")
            plt.show()
            st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot(PlotWordcloud())
    
except:
    print("error")