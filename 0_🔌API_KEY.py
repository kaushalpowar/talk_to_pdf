"""
API Key Configuration Page for Talk to PDF Application

This module handles the OpenAI API key configuration and validation for the Talk to PDF application.
It provides a user interface for API key input and manages the transition to the PDF upload page.
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

# Configuration constants
PAGE_TITLE = "Talk to PDF"
PAGE_ICON = ":robot_face:"
API_KEY_SESSION_KEY = 'api_key'

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
    Validate the provided OpenAI API key format.
    
    Args:
        api_key: The API key to validate
        
    Returns:
        bool: True if the API key format is valid, False otherwise
    """
    # Basic validation - check if key starts with 'sk-' and has sufficient length
    return bool(api_key and api_key.startswith('sk-') and len(api_key) > 20)

def setup_api_key(api_key: str) -> None:
    """
    Configure the OpenAI client with the provided API key.
    
    Args:
        api_key: The OpenAI API key to configure
    """
    openai.api_key = api_key
    st.session_state[API_KEY_SESSION_KEY] = api_key

def handle_api_key_submission() -> None:
    """Handle the API key submission and page transition."""
    if st.session_state.get(API_KEY_SESSION_KEY):
        st.sidebar.success("✅ API key entered successfully")
        # Add small delay for better user experience
        time.sleep(1.5)
        switch_page('upload pdf')

def render_api_key_input() -> Optional[str]:
    """
    Render the API key input form and handle submission.
    
    Returns:
        Optional[str]: The entered API key if valid, None otherwise
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

    if not validate_api_key(api_key):
        st.error("❌ Invalid API key format. Please check your API key.")
        return None

    return api_key

def main() -> None:
    """Main function to run the API key configuration page."""
    try:
        initialize_page()
        
        api_key = render_api_key_input()
        
        if api_key:
            setup_api_key(api_key)
            
            if st.button("Submit", use_container_width=True):
                handle_api_key_submission()
        
        # Render sidebar content
        sidebar_stuff1()

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.info("Please refresh the page and try again.")

if __name__ == "__main__":
    main()