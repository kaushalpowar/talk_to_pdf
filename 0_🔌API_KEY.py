"""
API Key Configuration Page for Talk to PDF Application

This module handles the OpenAI API key configuration and validation for the Talk to PDF application.
It provides a user interface for entering and validating API keys before proceeding to PDF upload.
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
OPENAI_API_URL = "https://platform.openai.com/account/api-keys"
PAGE_TITLE = "Talk to PDF"
PAGE_ICON = ":robot_face:"
MAIN_TITLE = "Talk to your PDF 🤖 📑️"
ERROR_MESSAGE = "⚠️ Please enter OpenAI API key"
SUCCESS_MESSAGE = "✅ API key entered successfully"
NEXT_PAGE = "upload pdf"
DELAY_SECONDS = 1.5

class APIKeyManager:
    """Handles API key validation and storage."""
    
    @staticmethod
    def validate_api_key(api_key: str) -> bool:
        """
        Validates the provided OpenAI API key.
        
        Args:
            api_key: The API key to validate
            
        Returns:
            bool: True if key is valid, False otherwise
        """
        if not api_key or len(api_key.strip()) == 0:
            return False
        
        # TODO: Implement actual API key validation by making a test request
        return True
    
    @staticmethod
    def save_api_key(api_key: str) -> None:
        """
        Saves the API key to session state and configures OpenAI.
        
        Args:
            api_key: The API key to save
        """
        st.session_state['api_key'] = api_key
        openai.api_key = api_key

class UIComponents:
    """Handles UI component rendering."""
    
    @staticmethod
    def setup_page() -> None:
        """Configures the page layout and title."""
        st.set_page_config(
            page_title=PAGE_TITLE,
            page_icon=PAGE_ICON,
            layout="wide"
        )
        st.title(MAIN_TITLE)
    
    @staticmethod
    def render_api_input() -> Optional[str]:
        """
        Renders the API key input field.
        
        Returns:
            Optional[str]: The entered API key or None
        """
        st.write("#### Enter your OpenAI api key below :")
        return st.text_input(
            f"Enter your OpenAI API key ({OPENAI_API_URL})",
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

def main():
    """Main application entry point."""
    
    # Setup page
    UIComponents.setup_page()
    
    # Get API key input
    api_key = UIComponents.render_api_input()
    
    # Handle API key validation
    if not APIKeyManager.validate_api_key(api_key):
        st.sidebar.warning(ERROR_MESSAGE)
    else:
        APIKeyManager.save_api_key(api_key)
    
    # Handle form submission
    if UIComponents.render_submit_button() and api_key:
        st.sidebar.success(SUCCESS_MESSAGE)
        time.sleep(DELAY_SECONDS)
        switch_page(NEXT_PAGE)
    
    # Render sidebar content
    sidebar_stuff1()

if __name__ == "__main__":
    main()