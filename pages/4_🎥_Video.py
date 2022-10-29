import streamlit as st

st.sidebar.success("Pilih Halaman Diatas")

st.title("Video")

try:
    searchVid = st.text_input("Masukan Link Video")
    st.video("https://youtu.be/"+searchVid, format="video/mp4", start_time=0)
except:
    print("error")