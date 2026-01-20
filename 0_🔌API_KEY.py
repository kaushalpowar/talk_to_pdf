"""
API Key Configuration Page for Talk to PDF Application

This module handles the initial setup and API key configuration for the Talk to PDF application.
It provides a user interface for entering and validating OpenAI API keys before proceeding
to the PDF upload functionality.
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
API_KEY_PROMPT = "Enter your OpenAI API key (https://platform.openai.com/account/api-keys)"
SUCCESS_MESSAGE = "✅ API key entered successfully"
WARNING_MESSAGE = "⚠️ Please enter OpenAI API key"

class APIKeyManager:
    """Manages the OpenAI API key configuration and validation."""
    
    @staticmethod
    def validate_api_key(api_key: str) -> bool:
        """
        Validates the provided OpenAI API key format.
        
        Args:
            api_key: The API key to validate
            
        Returns:
            bool: True if the key format is valid, False otherwise
        """
        return bool(api_key and api_key.startswith('sk-'))
    
    @staticmethod
    def save_api_key(api_key: str) -> None:
        """
        Saves the API key to session state and configures OpenAI.
        
        Args:
            api_key: The API key to save
        """
        st.session_state['api_key'] = api_key
        openai.api_key = api_key

def initialize_page() -> None:
    """Initializes the Streamlit page configuration."""
    st.set_page_config(
        page_title=TITLE,
        page_icon=PAGE_ICON,
        layout="wide"
    )
    st.title(TITLE)

def render_api_key_input() -> Optional[str]:
    """
    Renders the API key input form.
    
    Returns:
        Optional[str]: The entered API key if provided
    """
    st.write("#### Enter your OpenAI api key below :")
    return st.text_input(
        API_KEY_PROMPT,
        type="password",
        key="api_key_input"
    )

def handle_submit(api_key: str) -> None:
    """
    Handles the submit button action.
    
    Args:
        api_key: The entered API key
    """
    if st.button("Submit", use_container_width=True):
        if APIKeyManager.validate_api_key(api_key):
            st.sidebar.success(SUCCESS_MESSAGE)
            time.sleep(1.5)
            switch_page('upload pdf')
        else:
            st.error("Invalid API key format. Please check your key.")

def main() -> None:
    """Main function to run the API key configuration page."""
    try:
        initialize_page()
        
        # Render API key input
        api_key = render_api_key_input()
        
        # Handle API key state
        if not api_key:
            st.sidebar.warning(WARNING_MESSAGE)
        else:
            APIKeyManager.save_api_key(api_key)
            handle_submit(api_key)
        
        # Render sidebar content
        sidebar_stuff1()
        
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.error("Please refresh the page and try again.")

if __name__ == "__main__":
    main()