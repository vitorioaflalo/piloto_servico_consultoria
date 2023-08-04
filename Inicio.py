import streamlit as st
from PIL import Image

#/c/Users/vitor/anaconda3/python

st.set_page_config(
    page_title="Home",
    page_icon=":fork_and_knife_with_plate:",
    layout="wide",
)

image = Image.open('logo.png')

st.sidebar.image(image, width=120)

st.sidebar.markdown(' # Consultoria - CNPJs')
st.sidebar.markdown("""---""")
st.markdown(
"""
Consultoria Estratégica para o Mapeamento e Análise do Poder de Compras Governamental (Foco nas MPE’s).
"""
)
