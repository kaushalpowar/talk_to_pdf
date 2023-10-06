import os
from functions import sidebar_stuff2, query_engine, save_file, remove_file

import streamlit as st
from streamlit_extras.switch_page_button import switch_page

sidebar_stuff2()

pdf_file = st.file_uploader(
            "Unleash the power of AI to have a conversation with your PDFs and uncover new insights, all with a single upload⬇️ ",)
model_name = st.selectbox("Select the model you want to use",("gpt-3.5-turbo","gpt-4"))
temperature = st.slider("Set temperature", 0.1, 1.0, 0.5,0.1)

if pdf_file is not None:
    query_engine(pdf_file, model_name, temperature)
else:
        st.error("Please upload a PDF file")
