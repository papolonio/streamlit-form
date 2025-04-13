import streamlit as st
from dotenv import load_dotenv
from components.form import render_form

load_dotenv()

st.set_page_config(page_title="Formulário de Projeto", layout="centered", initial_sidebar_state="collapsed")
st.markdown("<style>body { background-color: #0e1117; color: white; }</style>", unsafe_allow_html=True)

st.title("Cadastro de Projeto")
render_form()
