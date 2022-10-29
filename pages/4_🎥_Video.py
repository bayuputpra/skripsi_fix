import streamlit as st

st.sidebar.success("Pilih Halaman Diatas")

st.title("Video")
class Format:
    end = '\033[0m'
    underline = '\033[4m'

try:
    searchVid = st.text_input("Masukan Link Video (https://www.youtube.com/watch?v="+Format.underline+"C7Ly_HN-OCQ)"+Format.end)
    st.video("https://youtu.be/"+searchVid, format="video/mp4", start_time=0)
except:
    print("error")