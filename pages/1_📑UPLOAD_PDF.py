import os
from functions import sidebar_stuff2, query_engine, save_file, remove_file, load_document
import tempfile

import streamlit as st
from streamlit_extras.switch_page_button import switch_page

# Set up the sidebar with model selection and temperature adjustment
sidebar_stuff2()

# Model selection dropdown
model_name = st.selectbox("Select the model you want to use", ("gpt-3.5-turbo", "gpt-4"))

# Temperature slider for response variability
temperature = st.slider("Set temperature", 0.1, 1.0, 0.5, 0.1)

# PDF file uploader with support for multiple files
pdf_file = st.file_uploader(
    "Unleash the power of AI to have a conversation with your PDFs and uncover new insights, all with a single upload⬇️ ",
    type=['pdf'],
    accept_multiple_files=True
)

# Process the uploaded PDF file
if pdf_file:
    reader = load_document(uploaded_files=pdf_file)
    query_engine = query_engine(reader, model_name, temperature)
else:
    st.error("Please upload a PDF file")