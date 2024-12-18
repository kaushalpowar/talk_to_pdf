"""
API Key Configuration Page for Talk to PDF Application.

This module handles the OpenAI API key configuration and validation
for the Talk to PDF application using Streamlit.
"""

import logging
from typing import Optional
import time
import tempfile
import os

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
API_KEY_LABEL = "Enter your OpenAI API key"
API_KEY_URL = "https://platform.openai.com/account/api-keys"
SUCCESS_MESSAGE = "✅ API key entered successfully"
ERROR_MESSAGE = "⚠️ Please enter OpenAI API key"

class APIKeyConfig:
    """Handles API key configuration and validation."""
    
    @staticmethod
    def validate_api_key(api_key: str) -> bool:
        """
        Validates the OpenAI API key format.
        
        Args:
            api_key: The API key to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        if not api_key:
            return False
        # Basic format validation - can be expanded
        return api_key.startswith('sk-') and len(api_key) > 20

    @staticmethod
    def save_api_key(api_key: str) -> None:
        """
        Saves the API key to session state and configures OpenAI.
        
        Args:
            api_key: The API key to save
        """
        st.session_state['api_key'] = api_key
        openai.api_key = api_key
        logger.info("API key configured successfully")

def initialize_page() -> None:
    """Initializes the Streamlit page configuration."""
    st.set_page_config(
        page_title=PAGE_TITLE,
        page_icon=PAGE_ICON,
        layout="wide"
    )
    st.title(TITLE_TEXT)

def render_api_key_input() -> Optional[str]:
    """
    Renders the API key input field.
    
    Returns:
        Optional[str]: The entered API key or None
    """
    st.write("#### Enter your OpenAI api key below :")
    return st.text_input(
        f"{API_KEY_LABEL} ({API_KEY_URL})",
        type="password",
        key="api_key_input"
    )

def handle_submit(api_key: str) -> None:
    """
    Handles the submit button click event.
    
    Args:
        api_key: The entered API key
    """
    if APIKeyConfig.validate_api_key(api_key):
        with st.spinner("Configuring API key..."):
            APIKeyConfig.save_api_key(api_key)
            st.sidebar.success(SUCCESS_MESSAGE)
            time.sleep(1.5)
            switch_page('upload pdf')
    else:
        st.error("Invalid API key format. Please check your API key.")

def main():
    """Main function to run the API key configuration page."""
    try:
        initialize_page()
        
        api_key = render_api_key_input()
        
        # Show warning if no API key
        if not api_key:
            st.sidebar.warning(ERROR_MESSAGE)
        
        # Submit button
        if st.button("Submit", use_container_width=True):
            handle_submit(api_key)
        
        # Render sidebar
        sidebar_stuff1()
        
    except Exception as e:
        logger.error(f"Error in API key configuration: {str(e)}")
        st.error("An error occurred. Please try again or contact support.")

if __name__ == "__main__":
    main()