import tweepy
import re
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import streamlit as st
import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize
import string

st.sidebar.success("Pilih Halaman Diatas")

api_key = "APfBI7D2yFcruynoBr4eYTuk2"
api_secret_key = "jX35Mj2ADJIS76FXl36fCIjHxvHliimL4fY3z6DKlUZ9Q5FrgC"
access_token = "3049333950-eGUOgNZ86LPxKvaCp8mKGODfCD2VzpbzdFOjEci"
access_token_secret = "V6v2pWhhVmpJb3KL3xMKlgA8i3w9toH4cScxOXAf39gR2"

auth = tweepy.OAuthHandler(api_key,api_secret_key)
auth.set_access_token(access_token,access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)

def main():
    st.title("Sentimen Analisis Twitter") 

    try:
        searchvalue = st.text_input("Masukan Topik Pembahasan Yang Dicari")
        searchcount = st.text_input("Masukan Jumlah Baris Yang Dicari")
        hasilSearch = tweepy.Cursor(api.search_tweets, q=searchvalue, lang='id', tweet_mode="extended").items(int(searchcount))

        hasilAnalisis = pd.DataFrame(columns=["tgl","user","text"])

        for tweet in hasilSearch:
            tgl = tweet.created_at
            user = tweet.user.screen_name
            text = tweet.text

            file=[tgl, user, text]
            hasilAnalisis.loc[len(hasilAnalisis)]=file

        hasilAnalisis.drop_duplicates(subset="text",keep="first",inplace=True)

        def preProcess(text):
            #removing number
            text=text.lower()
            text=re.sub(r"\d+","",text)
            #remove mention,link,hashtag
            text=" ".join(re.sub("([@#][A-Za-z0-9]+)|(\w+:\/\/\S+)"," ",text).split())
            #remove punctuation
            text=text.translate(text.maketrans("","",string.punctuation))
            #remove whitespace
            text=text.strip()
            space=text.split()
            text=word_tokenize(text)
            return text

        hasilAnalisis['text_clear']=hasilAnalisis['text'].apply(preProcess)

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
        
        results=hasilAnalisis['text_clear'].apply(sentiment_analysis_indonesia)
        results=list(zip(*results))
        hasilAnalisis['polarity_score']=results[0]
        hasilAnalisis['sentimen']=results[1]

        st.text("Dataset")
        hasilAnalisis.reset_index()
        st.write(hasilAnalisis)
        st.download_button(label="Download CSV", data=hasilAnalisis.to_csv(),mime="text/csv",file_name="data_tw.csv")

        tweet_positif = hasilAnalisis[hasilAnalisis["sentimen"]=="positif"]
        tweet_netral = hasilAnalisis[hasilAnalisis["sentimen"]=="netral"]
        tweet_negatif = hasilAnalisis[hasilAnalisis["sentimen"]=="negatif"]

        st.text("Hasil Sentimen")
        jmlA=len(tweet_positif)
        jmlB=len(tweet_netral)
        jmlC=len(tweet_negatif)
        persenA="{}%".format(100*len(tweet_positif)/len(hasilAnalisis))
        persenB="{}%".format(100*len(tweet_netral)/len(hasilAnalisis))
        persenC="{}%".format(100*len(tweet_negatif)/len(hasilAnalisis))
        df=pd.DataFrame({'sentimen':["positif","netral","negatif"],'jumlah':[jmlA,jmlB,jmlC],'persen':[persenA,persenB,persenC]})
        df

        st.text("Pie Chart")
        sentiment_counts = hasilAnalisis.groupby(["sentimen"]).size()
        fig,ax=plt.subplots()
        sentiment_counts.plot.pie(autopct='%1.1f%%', startangle=270, fontsize=12, label="")
        plt.figure(figsize=(6,6), dpi=100)
        ax.axis('equal')
        st.pyplot(fig)

        st.text("WordCloud")
        def PlotWordcloud():
            wordcloud = WordCloud(max_words=50, background_color="white", width=2500, height=2000).generate(str(hasilAnalisis["text"]))
            plt.imshow(wordcloud)
            plt.axis("off")
            plt.show()
            st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot(PlotWordcloud())
    except:
        print("error")

if __name__=='__main__':
        main()