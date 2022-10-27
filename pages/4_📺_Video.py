import streamlit as st

st.sidebar.success("Pilih Halaman Diatas")

Vid = st.title("Video")
st.video("https://www.youtube.com/watch?v="+Vid, format="video/mp4", start_time=0)
