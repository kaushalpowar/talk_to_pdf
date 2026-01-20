"""
API Key Configuration Page for Talk to PDF Application

This module handles the OpenAI API key input and validation for the Talk to PDF application.
It provides a user interface for entering and validating API keys before proceeding to
the PDF upload functionality.
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
TITLE_TEXT = "Talk to your PDF 🤖 📑️"
API_KEY_LABEL = "Enter your OpenAI API key (https://platform.openai.com/account/api-keys)"
SUCCESS_MESSAGE = "✅ API key entered successfully"
WARNING_MESSAGE = "⚠️ Please enter OpenAI API key"

def initialize_page() -> None:
    """Initialize the Streamlit page configuration and title."""
    st.set_page_config(
        page_title=PAGE_TITLE,
        page_icon=PAGE_ICON,
        layout="wide"
    )
    st.title(TITLE_TEXT)

def validate_api_key(api_key: str) -> bool:
    """
    Validate the provided OpenAI API key format.
    
    Args:
        api_key: The API key to validate
        
    Returns:
        bool: True if the key format is valid, False otherwise
    """
    # Basic validation - check if key starts with 'sk-' and has sufficient length
    return bool(api_key and api_key.startswith('sk-') and len(api_key) > 20)

def save_api_key(api_key: str) -> None:
    """
    Save the API key to session state and configure OpenAI.
    
    Args:
        api_key: The API key to save
    """
    st.session_state['api_key'] = api_key
    openai.api_key = api_key

def handle_api_key_submission() -> None:
    """Handle the API key submission and navigation logic."""
    if st.session_state.get('api_key'):
        st.sidebar.success(SUCCESS_MESSAGE)
        time.sleep(1.5)
        switch_page('upload pdf')

def create_api_key_input() -> Optional[str]:
    """
    Create and display the API key input field.
    
    Returns:
        Optional[str]: The entered API key if provided
    """
    st.write("#### Enter your OpenAI api key below :")
    return st.text_input(
        API_KEY_LABEL,
        type="password",
        help="Your API key will be stored securely in the session state"
    )

def main() -> None:
    """Main function to run the API key configuration page."""
    initialize_page()
    
    # Create API key input
    api_key = create_api_key_input()
    
    # Handle API key presence/absence
    if not api_key:
        st.sidebar.warning(WARNING_MESSAGE)
    else:
        # Validate and save API key
        if validate_api_key(api_key):
            save_api_key(api_key)
        else:
            st.error("Invalid API key format. Please check your key.")
    
    # Create submit button
    submit = st.button("Submit", use_container_width=True)
    
    # Handle submission
    if submit and api_key:
        handle_api_key_submission()
    
    # Display sidebar content
    sidebar_stuff1()

if __name__ == "__main__":
    main()