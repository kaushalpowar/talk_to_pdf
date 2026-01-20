"""
API Key Configuration Module for Talk to PDF Application

This module handles the initial setup and configuration of the OpenAI API key
for the Talk to PDF application. It provides a user interface for API key input
and validation using Streamlit.
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
API_KEY_PLACEHOLDER = "Enter your OpenAI API key (https://platform.openai.com/account/api-keys)"
SUCCESS_MESSAGE = "✅ API key entered successfully"
WARNING_MESSAGE = "⚠️ Please enter OpenAI API key"

def initialize_page_config() -> None:
    """Initialize Streamlit page configuration."""
    st.set_page_config(
        page_title="Talk to PDF",
        page_icon=":robot_face:",
        layout="wide"
    )

def setup_api_key() -> Optional[str]:
    """
    Handle API key input and validation.
    
    Returns:
        Optional[str]: The validated API key or None if not provided
    """
    st.title(TITLE)
    st.write("#### Enter your OpenAI api key below :")
    
    api_key = st.text_input(
        API_KEY_PLACEHOLDER,
        type="password"
    )
    
    # Store API key in session state
    st.session_state['api_key'] = api_key
    
    if not api_key:
        st.sidebar.warning(WARNING_MESSAGE)
        return None
    
    try:
        openai.api_key = api_key
        return api_key
    except Exception as e:
        st.error(f"Error setting API key: {str(e)}")
        return None

def handle_submit() -> None:
    """Handle the submit button click event."""
    submit = st.button("Submit", use_container_width=True)
    
    if submit and st.session_state.get('api_key'):
        st.sidebar.success(SUCCESS_MESSAGE)
        # Add small delay for better UX
        time.sleep(1.5)
        switch_page('upload pdf')

def main() -> None:
    """Main function to run the API key configuration page."""
    try:
        # Initialize page configuration
        initialize_page_config()
        
        # Setup API key
        api_key = setup_api_key()
        
        # Handle form submission
        handle_submit()
        
        # Setup sidebar
        sidebar_stuff1()
        
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        # TODO: Add proper error logging
        
if __name__ == "__main__":
    main()