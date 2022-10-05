from cProfile import label
from click import ClickException
import tweepy
import re
from textblob import TextBlob
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import streamlit as st

api_key = "APfBI7D2yFcruynoBr4eYTuk2"
api_secret_key = "jX35Mj2ADJIS76FXl36fCIjHxvHliimL4fY3z6DKlUZ9Q5FrgC"
access_token = "3049333950-eGUOgNZ86LPxKvaCp8mKGODfCD2VzpbzdFOjEci"
access_token_secret = "V6v2pWhhVmpJb3KL3xMKlgA8i3w9toH4cScxOXAf39gR2"

auth = tweepy.OAuthHandler(api_key,api_secret_key)
auth.set_access_token(access_token,access_token_secret)
api = tweepy.API(auth)

def main():
    st.title("Sentiment Analysis of tweets")
    
if __name__=='__main__':
        main()

try:
    searchvalue = st.text_input("Masukan Topik Pembahasan Yang Dicari")
    searchcount = st.text_input("Masukan Jumlah Baris Yang Dicari")
    hasilSearch  = api.search_tweets(q=searchvalue, count = int(searchcount), lang='id')

    hasilAnalisis = pd.DataFrame(columns=["tgl","user","text","sentimen"])

    for tweet in hasilSearch:
        tgl = tweet.created_at
        user = tweet.user.screen_name
        text = tweet.text
        tweet_clear = " ".join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\s+)"," ", tweet.text).split())

        try:
            analysis = TextBlob(tweet_clear)
        except:
            print("error")

        try:
            analysis = analysis.translate(from_lang="id", to="en")
        except Exception as e:
            print(e)

        if analysis.sentiment.polarity > 0.0:
            sentimen = "positif"
        elif analysis.sentiment.polarity == 0.0:
            sentimen = "netral"
        else:
            sentimen = "negatif"
        
        file=[tgl, user, text, sentimen]
        hasilAnalisis.loc[len(hasilAnalisis)]=file

    hasilAnalisis.drop_duplicates(subset="text",keep="first",inplace=True)
    st.text("Dataset")
    st.write(hasilAnalisis)
    button_csv=st.download_button(
        label="Download CSV", 
        data=hasilAnalisis.to_csv(),
        mime="text/csv",
        file_name="data_tw.csv"
    )
    from acc import acc
    st.text(acc())

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