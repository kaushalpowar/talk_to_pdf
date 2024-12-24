"""
API Key Configuration Page for Talk to PDF Application

This module handles the OpenAI API key input and validation for the Talk to PDF application.
It provides a user interface for entering and validating API keys before proceeding to
the PDF upload functionality.
"""

import logging
from typing import Optional
import time

import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import openai
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    ServiceContext,
    set_global_service_context
)
from llama_index.llms.openai import OpenAI

from functions import sidebar_stuff1

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
PAGE_TITLE = "Talk to PDF"
PAGE_ICON = ":robot_face:"
TITLE_TEXT = "Talk to your PDF 🤖 📑️"
API_KEY_LABEL = "Enter your OpenAI API key (https://platform.openai.com/account/api-keys)"
API_KEY_HEADER = "#### Enter your OpenAI api key below :"
SUCCESS_MESSAGE = "✅ API key entered successfully"
WARNING_MESSAGE = "⚠️ Please enter OpenAI API key"

def initialize_page_config() -> None:
    """Initialize Streamlit page configuration."""
    st.set_page_config(
        page_title=PAGE_TITLE,
        page_icon=PAGE_ICON,
        layout="wide"
    )
    st.title(TITLE_TEXT)

def validate_api_key(api_key: str) -> bool:
    """
    Validate the OpenAI API key format and basic structure.
    
    Args:
        api_key: The API key to validate
        
    Returns:
        bool: True if the key appears valid, False otherwise
    """
    if not api_key:
        return False
    
    # Basic validation - check if key starts with expected prefix
    # and meets minimum length requirements
    return (
        api_key.startswith(('sk-', 'org-')) and 
        len(api_key) > 20
    )

def handle_api_key_submission(api_key: str) -> None:
    """
    Handle the API key submission process.
    
    Args:
        api_key: The submitted API key
    """
    try:
        if validate_api_key(api_key):
            openai.api_key = api_key
            st.sidebar.success(SUCCESS_MESSAGE)
            logger.info("API key successfully configured")
            
            # Add delay for better UX
            time.sleep(1.5)
            switch_page('upload pdf')
        else:
            st.error("Invalid API key format. Please check your key and try again.")
            logger.warning("Invalid API key format attempted")
    except Exception as e:
        st.error(f"Error configuring API key: {str(e)}")
        logger.error(f"API key configuration error: {str(e)}")

def main():
    """Main application function."""
    try:
        initialize_page_config()

        # API Key Input Section
        st.write(API_KEY_HEADER)
        api_key = st.text_input(
            API_KEY_LABEL,
            type="password",
            help="Your OpenAI API key is required to process PDF documents"
        )

        # Store API key in session state
        st.session_state['api_key'] = api_key

        # Show warning if no API key is entered
        if not api_key:
            st.sidebar.warning(WARNING_MESSAGE)
        
        # Submit button with full width
        if st.button("Submit", use_container_width=True):
            handle_api_key_submission(api_key)

        # Display sidebar content
        sidebar_stuff1()

    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        st.error("An unexpected error occurred. Please try again later.")

if __name__ == "__main__":
    main()