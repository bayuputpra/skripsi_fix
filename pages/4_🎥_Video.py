import streamlit as st

st.sidebar.success("Pilih Halaman Diatas")

def main():
    st.title("Video")

if __name__=='__main__':
    main()

try:
    searchVid = st.text_input("Masukan Link Video")
    video="https://www.youtube.com/watch?v="+searchVid
    st.video(video, format="video/mp4", start_time=0)
except:
    print("error")