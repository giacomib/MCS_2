import streamlit as st
from PIL import Image
import my_library

st.set_page_config(layout="wide")

with st.container():
   st.title('Progetto 2')

   col1, col2 = st.columns([0.5, 0.5], gap = "medium")

uploaded_file = st.sidebar.file_uploader("Scegliere l'immagine", type = "bmp")

f_value = st.sidebar.number_input("Selezionare il valore di F", value = 10, min_value = 0)

d_value = st.sidebar.number_input("Selezionare il valore di d", value = 9, min_value = 0)

if d_value > (2*f_value)-2:
   st.error('Attenzione: il valore di d non è valido')

if uploaded_file is not None:
   image_fore = Image.open("data/" + uploaded_file.name)
   image_after = my_library.run(image_fore, f_value, d_value)
   with col1:
      st.header("Prima")
      st.image(image_fore, output_format = "auto", use_column_width = "always")

   with col2:
      st.header("Dopo")
      st.image(image_after, output_format = "auto", use_column_width = "always")