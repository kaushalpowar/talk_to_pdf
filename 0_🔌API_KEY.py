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

from functions import sidebar_stuff1

# Constants
PAGE_TITLE = "Talk to PDF"
PAGE_ICON = ":robot_face:"
API_KEY_SESSION_KEY = 'api_key'

class APIKeyManager:
    """Handles OpenAI API key validation and management."""
    
    @staticmethod
    def validate_api_key(api_key: str) -> bool:
        """
        Validates the provided OpenAI API key.
        
        Args:
            api_key: The API key to validate
            
        Returns:
            bool: True if key is valid (not empty), False otherwise
        """
        return bool(api_key and api_key.strip())
    
    @staticmethod
    def save_api_key(api_key: str) -> None:
        """
        Saves the API key to session state and configures OpenAI.
        
        Args:
            api_key: The API key to save
        """
        st.session_state[API_KEY_SESSION_KEY] = api_key
        openai.api_key = api_key

class PageUI:
    """Handles UI components and layout for the API key configuration page."""
    
    @staticmethod
    def setup_page():
        """Configures initial page settings and layout."""
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
            "Enter your OpenAI API key (https://platform.openai.com/account/api-keys)",
            type="password"
        )
    
    @staticmethod
    def handle_submission(api_key: str):
        """
        Handles the API key submission process.
        
        Args:
            api_key: The API key to process
        """
        submit = st.button("Submit", use_container_width=True)
        
        if not api_key:
            st.sidebar.warning("⚠️ Please enter OpenAI API key")
        
        if submit and api_key:
            st.sidebar.success("✅ API key entered successfully")
            time.sleep(1.5)
            switch_page('upload pdf')

def main():
    """Main function to run the API key configuration page."""
    # Initialize components
    page_ui = PageUI()
    api_manager = APIKeyManager()
    
    # Setup page
    page_ui.setup_page()
    
    try:
        # Render API key input and handle submission
        api_key = page_ui.render_api_key_input()
        
        if api_key:
            api_manager.save_api_key(api_key)
        
        page_ui.handle_submission(api_key)
        
        # Render sidebar content
        sidebar_stuff1()
        
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        # TODO: Add proper error logging
        
if __name__ == "__main__":
    main()