"""
API Key Configuration Module for Talk to PDF Application

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

# Constants
TITLE = "Talk to your PDF 🤖 📑️"
PAGE_ICON = ":robot_face:"
API_KEY_PLACEHOLDER = "Enter your OpenAI API key (https://platform.openai.com/account/api-keys)"
SUCCESS_MESSAGE = "✅ API key entered successfully"
WARNING_MESSAGE = "⚠️ Please enter OpenAI API key"
NEXT_PAGE = "upload pdf"
TRANSITION_DELAY = 1.5

def initialize_page_config() -> None:
    """Initialize Streamlit page configuration with title and layout settings."""
    st.set_page_config(
        page_title="Talk to PDF",
        page_icon=PAGE_ICON,
        layout="wide"
    )
    st.title(TITLE)

def validate_api_key(api_key: str) -> bool:
    """
    Validate the provided OpenAI API key.

    Args:
        api_key (str): The API key to validate

    Returns:
        bool: True if the API key is valid, False otherwise
    """
    if not api_key:
        return False
    
    # TODO: Add actual API key validation by making a test request to OpenAI
    return True

def handle_api_key_submission() -> None:
    """Handle the API key input and submission process."""
    st.write("#### Enter your OpenAI api key below :")
    
    # API key input with password protection
    api_key = st.text_input(
        API_KEY_PLACEHOLDER,
        type="password",
        key="api_key_input"
    )
    
    # Store API key in session state
    st.session_state['api_key'] = api_key
    
    # Display warning if API key is missing
    if not api_key:
        st.sidebar.warning(WARNING_MESSAGE)
    else:
        try:
            openai.api_key = api_key
        except Exception as e:
            st.error(f"Error setting API key: {str(e)}")
            return

    # Handle submit button
    if st.button("Submit", use_container_width=True):
        if validate_api_key(api_key):
            st.sidebar.success(SUCCESS_MESSAGE)
            time.sleep(TRANSITION_DELAY)
            switch_page(NEXT_PAGE)
        else:
            st.error("Invalid API key. Please check and try again.")

def main():
    """Main function to run the API key configuration interface."""
    try:
        # Initialize page configuration
        initialize_page_config()
        
        # Handle API key submission
        handle_api_key_submission()
        
        # Display sidebar content
        sidebar_stuff1()
        
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        # TODO: Add proper error logging
        
if __name__ == "__main__":
    main()