"""
API Key Configuration Module for Talk to PDF Application

This module handles the initial setup and configuration of the OpenAI API key
for the Talk to PDF application. It provides a secure interface for users to
input their API key and manages the application state accordingly.
"""

import os
import time
from typing import Optional

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

# Constants
TITLE = "Talk to your PDF 🤖 📑️"
API_KEY_URL = "https://platform.openai.com/account/api-keys"
SUCCESS_MESSAGE = "✅ API key entered successfully"
WARNING_MESSAGE = "⚠️ Please enter OpenAI API key"

def initialize_page_config() -> None:
    """Initialize Streamlit page configuration."""
    st.set_page_config(
        page_title="Talk to PDF",
        page_icon=":robot_face:",
        layout="wide"
    )
    st.title(TITLE)

def setup_api_key_input() -> Optional[str]:
    """
    Set up the API key input field and handle its state.
    
    Returns:
        Optional[str]: The entered API key or None if not provided
    """
    st.write("#### Enter your OpenAI api key below :")
    api_key = st.text_input(
        f"Enter your OpenAI API key ({API_KEY_URL})",
        type="password"
    )
    
    # Store API key in session state
    st.session_state['api_key'] = api_key
    
    return api_key

def handle_api_key_submission(api_key: Optional[str]) -> None:
    """
    Handle the API key submission and validation.
    
    Args:
        api_key (Optional[str]): The API key to validate
    """
    if not api_key:
        st.sidebar.warning(WARNING_MESSAGE)
    else:
        try:
            # Set API key for OpenAI
            openai.api_key = api_key
            
            # Handle submission button
            if st.button("Submit", use_container_width=True):
                st.sidebar.success(SUCCESS_MESSAGE)
                # Add small delay for better UX
                time.sleep(1.5)
                switch_page('upload pdf')
                
        except Exception as e:
            st.error(f"Error setting API key: {str(e)}")
            st.session_state['api_key'] = None

def main():
    """Main function to run the API key configuration page."""
    try:
        # Initialize page
        initialize_page_config()
        
        # Setup API key input
        api_key = setup_api_key_input()
        
        # Handle API key submission
        handle_api_key_submission(api_key)
        
        # Setup sidebar
        sidebar_stuff1()
        
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.info("Please refresh the page and try again.")

if __name__ == "__main__":
    main()