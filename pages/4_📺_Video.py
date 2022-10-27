import streamlit as st

st.sidebar.success("Pilih Halaman Diatas")

def main():
    st.title("Video")

searchVid = st.text_input("Masukan Link Video")
st.video("https://www.youtube.com/watch?v="+searchVid, format="video/mp4", start_time=0)