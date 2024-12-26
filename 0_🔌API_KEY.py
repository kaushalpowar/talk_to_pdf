"""
API Key Configuration Page for Talk to PDF Application

This module handles the initial setup and API key configuration for the Talk to PDF application.
It provides a secure interface for users to input their OpenAI API key and manages the transition
to the PDF upload page once properly configured.
"""

import os
import time
from typing import Optional

import openai
import streamlit as st
from streamlit_extras.switch_page_button import switch_page

from functions import sidebar_stuff1

# Constants
OPENAI_API_KEY_ENV = "OPENAI_API_KEY"
PAGE_TITLE = "Talk to PDF"
PAGE_ICON = ":robot_face:"


class APIKeyManager:
    """Manages OpenAI API key configuration and validation."""
    
    @staticmethod
    def get_api_key() -> Optional[str]:
        """
        Retrieves API key from environment variables if available.
        
        Returns:
            Optional[str]: The API key if found in environment, None otherwise
        """
        return os.getenv(OPENAI_API_KEY_ENV)
    
    @staticmethod
    def validate_api_key(api_key: str) -> bool:
        """
        Validates the provided OpenAI API key format.
        
        Args:
            api_key (str): The API key to validate
            
        Returns:
            bool: True if key format is valid, False otherwise
        """
        # Basic validation - check if key starts with expected prefix
        return bool(api_key and api_key.startswith(("sk-", "org-")))


class PageConfig:
    """Handles page configuration and UI setup."""
    
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
    def show_api_input() -> str:
        """
        Displays API key input field and handles user input.
        
        Returns:
            str: User input API key
        """
        st.write("#### Enter your OpenAI API key below:")
        return st.text_input(
            "Enter your OpenAI API key (https://platform.openai.com/account/api-keys)",
            type="password",
            help="Your API key will be stored securely in the session state"
        )


def main():
    """Main application entry point."""
    # Initialize page configuration
    PageConfig.setup_page()
    
    # Setup API key manager
    api_manager = APIKeyManager()
    
    # Check for existing API key in environment
    env_api_key = api_manager.get_api_key()
    if env_api_key:
        st.info("API key found in environment variables")
        api_key = env_api_key
    else:
        # Get API key from user input
        api_key = PageConfig.show_api_input()
    
    # Store API key in session state
    st.session_state['api_key'] = api_key
    
    # Handle API key validation and configuration
    if not api_key:
        st.sidebar.warning("⚠️ Please enter OpenAI API key")
    else:
        try:
            if api_manager.validate_api_key(api_key):
                openai.api_key = api_key
                submit = st.button("Submit", use_container_width=True)
                
                if submit:
                    st.sidebar.success("✅ API key entered successfully")
                    # Add slight delay for better UX
                    time.sleep(1.5)
                    switch_page('upload pdf')
            else:
                st.error("Invalid API key format. Please check your key and try again.")
        except Exception as e:
            st.error(f"Error configuring API key: {str(e)}")
    
    # Setup sidebar
    sidebar_stuff1()


if __name__ == "__main__":
    main()