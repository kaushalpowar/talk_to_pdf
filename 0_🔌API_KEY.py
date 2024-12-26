"""
API Key Configuration Page for Talk to PDF Application

This module handles the OpenAI API key configuration and validation for the Talk to PDF application.
It provides a user interface for API key input and manages the transition to the PDF upload page
once the key is successfully validated.
"""

import time
from typing import Optional

import openai
import streamlit as st
from streamlit_extras.switch_page_button import switch_page

from functions import sidebar_stuff1
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    ServiceContext,
    set_global_service_context
)
from llama_index.llms.openai import OpenAI

# Configuration Constants
PAGE_TITLE = "Talk to PDF"
PAGE_ICON = ":robot_face:"
API_KEY_PLACEHOLDER = "Enter your OpenAI API key (https://platform.openai.com/account/api-keys)"
SUCCESS_MESSAGE = "✅ API key entered successfully"
WARNING_MESSAGE = "⚠️ Please enter OpenAI API key"
REDIRECT_DELAY = 1.5

class APIKeyManager:
    """Manages the OpenAI API key configuration and validation."""
    
    @staticmethod
    def validate_api_key(api_key: str) -> bool:
        """
        Validates the provided OpenAI API key.
        
        Args:
            api_key: The API key to validate
            
        Returns:
            bool: True if the key is not empty, False otherwise
        """
        return bool(api_key and api_key.strip())
    
    @staticmethod
    def save_api_key(api_key: str) -> None:
        """
        Saves the API key to session state and configures OpenAI.
        
        Args:
            api_key: The API key to save
        """
        st.session_state['api_key'] = api_key
        openai.api_key = api_key

class PageConfig:
    """Handles page configuration and UI setup."""
    
    @staticmethod
    def setup_page() -> None:
        """Configures the Streamlit page settings."""
        st.set_page_config(
            page_title=PAGE_TITLE,
            page_icon=PAGE_ICON,
            layout="wide"
        )
        st.title("Talk to your PDF 🤖 📑️")
    
    @staticmethod
    def render_api_key_input() -> Optional[str]:
        """
        Renders the API key input field.
        
        Returns:
            Optional[str]: The entered API key or None
        """
        st.write("#### Enter your OpenAI api key below :")
        return st.text_input(
            API_KEY_PLACEHOLDER,
            type="password"
        )
    
    @staticmethod
    def render_submit_button() -> bool:
        """
        Renders the submit button.
        
        Returns:
            bool: True if button is clicked, False otherwise
        """
        return st.button("Submit", use_container_width=True)

def main() -> None:
    """Main function to run the API key configuration page."""
    
    # Initialize page configuration
    page_config = PageConfig()
    page_config.setup_page()
    
    # Initialize API key manager
    api_manager = APIKeyManager()
    
    # Render API key input
    api_key = page_config.render_api_key_input()
    
    # Handle API key validation
    if not api_manager.validate_api_key(api_key):
        st.sidebar.warning(WARNING_MESSAGE)
    else:
        api_manager.save_api_key(api_key)
    
    # Handle form submission
    if page_config.render_submit_button() and api_key:
        st.sidebar.success(SUCCESS_MESSAGE)
        time.sleep(REDIRECT_DELAY)
        switch_page('upload pdf')
    
    # Render sidebar content
    sidebar_stuff1()

if __name__ == "__main__":
    main()