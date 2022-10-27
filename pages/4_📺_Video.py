import streamlit as st

st.sidebar.success("Pilih Halaman Diatas")

def main():
    st.title("Video")

Vid=""
st.video("https://www.youtube.com/watch?v="+Vid, format="video/mp4", start_time=0)

if __name__=='__main__':
        main()