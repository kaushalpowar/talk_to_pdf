"""
Talk to PDF - API Key Configuration Page

This module handles the initial setup of the OpenAI API key for the Talk to PDF application.
It provides a secure interface for users to input their API key and validates it before
allowing access to the PDF processing features.
"""

import os
import time
from typing import Optional

import openai
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    ServiceContext,
    set_global_service_context
)
from llama_index.llms.openai import OpenAI

from functions import sidebar_stuff1

# Constants
PAGE_TITLE = "Talk to PDF"
PAGE_ICON = ":robot_face:"
API_KEY_SESSION_KEY = 'api_key'
NEXT_PAGE = 'upload pdf'
SUCCESS_DELAY = 1.5

def initialize_page() -> None:
    """Initialize the Streamlit page configuration and title."""
    st.set_page_config(
        page_title=PAGE_TITLE,
        page_icon=PAGE_ICON,
        layout="wide"
    )
    st.title("Talk to your PDF 🤖 📑️")

def validate_api_key(api_key: str) -> bool:
    """
    Validate the provided OpenAI API key.
    
    Args:
        api_key: The API key to validate
        
    Returns:
        bool: True if the key is valid, False otherwise
    """
    if not api_key:
        return False
    
    # TODO: Add actual API key validation by making a test request to OpenAI
    return True

def handle_api_key_input() -> Optional[str]:
    """
    Handle the API key input form and validation.
    
    Returns:
        Optional[str]: The validated API key or None if invalid
    """
    st.write("#### Enter your OpenAI api key below :")
    api_key = st.text_input(
        "Enter your OpenAI API key (https://platform.openai.com/account/api-keys)",
        type="password",
        help="Your API key will be stored securely in the session state"
    )
    
    if not api_key:
        st.sidebar.warning("⚠️ Please enter OpenAI API key")
        return None
        
    return api_key

def setup_openai_client(api_key: str) -> None:
    """
    Configure the OpenAI client with the provided API key.
    
    Args:
        api_key: The OpenAI API key to use
    """
    openai.api_key = api_key
    st.session_state[API_KEY_SESSION_KEY] = api_key

def handle_submit_button(api_key: str) -> None:
    """
    Handle the submit button click event.
    
    Args:
        api_key: The API key to process
    """
    submit = st.button("Submit", use_container_width=True)
    if submit and validate_api_key(api_key):
        st.sidebar.success("✅ API key entered successfully")
        time.sleep(SUCCESS_DELAY)
        switch_page(NEXT_PAGE)

def main() -> None:
    """Main application entry point."""
    try:
        initialize_page()
        
        api_key = handle_api_key_input()
        if api_key:
            setup_openai_client(api_key)
            handle_submit_button(api_key)
        
        # Initialize sidebar content
        sidebar_stuff1()
        
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        # TODO: Add proper error logging
        
if __name__ == "__main__":
    main()