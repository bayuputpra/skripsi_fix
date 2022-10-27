import streamlit as st

st.sidebar.success("Pilih Halaman Diatas")

def main():
    st.title("Video")

Vid = st.text_input("Masukan Link Video")
st.video("https://www.youtube.com/watch?v="+Vid, format="video/mp4", start_time=0)