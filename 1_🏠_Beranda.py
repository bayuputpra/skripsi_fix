import streamlit as st

st.set_page_config(
	page_title="Skripsi",
)
st.title("Judul Skripsi")
st.image("logo.png",width=300)
st.sidebar.success("Pilih Halaman Diatas")
hide_st_style="""
        <style>
        #MainMenu {visibility:hidden;}
        </style>
        """
st.markdown(hide_st_style,unsafe_allow_html=True)