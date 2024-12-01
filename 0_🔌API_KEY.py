import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import os
import time
import tempfile
import openai
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, ServiceContext, set_global_service_context
from llama_index.llms.openai import OpenAI
from functions import sidebar_stuff1

# Set the page configuration for the Streamlit app
st.set_page_config(page_title="Talk to PDF", page_icon=":robot_face:", layout="wide")
st.title("Talk to your PDF 🤖 📑️")

# Prompt the user to enter their OpenAI API key
st.write("#### Enter your OpenAI API key below:")
api_key = st.text_input("Enter your OpenAI API key (https://platform.openai.com/account/api-keys)", type="password")
st.session_state['api_key'] = api_key

# Check if the API key is provided
if not api_key:
    st.sidebar.warning("⚠️ Please enter OpenAI API key")
else:
    openai.api_key = api_key

# Button to submit the API key
submit = st.button("Submit", use_container_width=True)
if submit:
    st.sidebar.success("✅ API key entered successfully")
    time.sleep(1.5)  # Delay for user experience
    switch_page('upload pdf')  # Navigate to the upload PDF page

# Call the sidebar function for additional UI elements
sidebar_stuff1()