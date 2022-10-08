from requests import options
import streamlit as st
from streamlit_option_menu import option_menu

with st.sidebar:
	selected=option_menu(
		menu_title="Main Menu",
		options=["Beranda","Sentimen","Akurasi"],
		icons=["house","emoticon","accuracy"],
		menu_icon="cast",
		default_index=0,
		page_title="Skripsi",
	)
st.title("Judul Skripsi")
st.image("logo.png")
st.sidebar.success("Pilih Halaman Diatas")