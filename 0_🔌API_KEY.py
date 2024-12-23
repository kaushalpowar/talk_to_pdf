"""
API Key Configuration Module for Talk to PDF Application

This module handles the OpenAI API key configuration and validation for the Talk to PDF application.
It provides a streamlit-based interface for users to input their API keys and manages the configuration
state throughout the application lifecycle.
"""

import os
import time
from dataclasses import dataclass
from typing import Optional

import openai
import streamlit as st
from streamlit_extras.switch_page_button import switch_page

from functions import sidebar_stuff1

# Constants
TITLE = "Talk to your PDF 🤖 📑️"
API_KEY_LABEL = "Enter your OpenAI API key (https://platform.openai.com/account/api-keys)"
WARNING_MESSAGE = "⚠️ Please enter OpenAI API key"
SUCCESS_MESSAGE = "✅ API key entered successfully"
NEXT_PAGE = "upload pdf"
REDIRECT_DELAY = 1.5

@dataclass
class AppConfig:
    """Configuration settings for the application."""
    page_title: str = "Talk to PDF"
    page_icon: str = ":robot_face:"
    layout: str = "wide"

class APIKeyManager:
    """Manages OpenAI API key validation and configuration."""
    
    @staticmethod
    def validate_api_key(api_key: str) -> bool:
        """
        Validates the provided OpenAI API key format.
        
        Args:
            api_key: The API key to validate
            
        Returns:
            bool: True if key format is valid, False otherwise
        """
        if not api_key:
            return False
        # Basic format validation - can be enhanced based on OpenAI's key format
        return len(api_key.strip()) > 0

    @staticmethod
    def configure_api_key(api_key: str) -> None:
        """
        Configures the OpenAI client with the provided API key.
        
        Args:
            api_key: The API key to configure
        """
        openai.api_key = api_key
        st.session_state['api_key'] = api_key

class UIManager:
    """Handles UI components and interactions."""
    
    @staticmethod
    def setup_page(config: AppConfig) -> None:
        """
        Configures the Streamlit page settings.
        
        Args:
            config: AppConfig instance containing page settings
        """
        st.set_page_config(
            page_title=config.page_title,
            page_icon=config.page_icon,
            layout=config.layout
        )
        st.title(TITLE)

    @staticmethod
    def render_api_key_input() -> Optional[str]:
        """
        Renders the API key input field.
        
        Returns:
            Optional[str]: The entered API key or None
        """
        st.write("#### Enter your OpenAI api key below :")
        return st.text_input(API_KEY_LABEL, type="password")

    @staticmethod
    def handle_submission(api_key: str) -> None:
        """
        Handles the API key submission process.
        
        Args:
            api_key: The submitted API key
        """
        submit = st.button("Submit", use_container_width=True)
        
        if not api_key:
            st.sidebar.warning(WARNING_MESSAGE)
        
        if submit and api_key:
            if APIKeyManager.validate_api_key(api_key):
                APIKeyManager.configure_api_key(api_key)
                st.sidebar.success(SUCCESS_MESSAGE)
                time.sleep(REDIRECT_DELAY)
                switch_page(NEXT_PAGE)
            else:
                st.error("Invalid API key format. Please check your key and try again.")

def main():
    """Main application entry point."""
    try:
        # Initialize application configuration
        config = AppConfig()
        
        # Setup UI components
        UIManager.setup_page(config)
        
        # Render API key input and handle submission
        api_key = UIManager.render_api_key_input()
        UIManager.handle_submission(api_key)
        
        # Render sidebar content
        sidebar_stuff1()
        
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        # TODO: Add proper error logging
        
if __name__ == "__main__":
    main()