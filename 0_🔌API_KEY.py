"""
API Key Configuration Page for Talk to PDF Application

This module handles the OpenAI API key configuration and validation for the Talk to PDF application.
It provides a user interface for entering and validating API keys using Streamlit.
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
TITLE_TEXT = "Talk to your PDF 🤖 📑️"
API_KEY_URL = "https://platform.openai.com/account/api-keys"


class APIKeyManager:
    """Manages OpenAI API key configuration and validation."""
    
    @staticmethod
    def validate_api_key(api_key: str) -> bool:
        """
        Validates the provided OpenAI API key format.
        
        Args:
            api_key: The API key to validate
            
        Returns:
            bool: True if the key format is valid, False otherwise
        """
        # Basic format validation - can be enhanced based on OpenAI's key format
        return bool(api_key and api_key.startswith("sk-") and len(api_key) > 20)

    @staticmethod
    def save_api_key(api_key: str) -> None:
        """
        Saves the API key to session state and configures OpenAI.
        
        Args:
            api_key: The API key to save
        """
        st.session_state['api_key'] = api_key
        openai.api_key = api_key


class StreamlitUI:
    """Handles Streamlit UI components and layout."""
    
    @staticmethod
    def setup_page() -> None:
        """Configures the Streamlit page settings."""
        st.set_page_config(
            page_title=PAGE_TITLE,
            page_icon=PAGE_ICON,
            layout="wide"
        )
        st.title(TITLE_TEXT)

    @staticmethod
    def render_api_key_input() -> Optional[str]:
        """
        Renders the API key input field.
        
        Returns:
            Optional[str]: The entered API key or None
        """
        st.write("#### Enter your OpenAI api key below :")
        return st.text_input(
            f"Enter your OpenAI API key ({API_KEY_URL})",
            type="password",
            value=os.getenv(OPENAI_API_KEY_ENV, "")
        )

    @staticmethod
    def show_feedback(api_key: str) -> None:
        """
        Shows appropriate feedback based on API key status.
        
        Args:
            api_key: The current API key
        """
        if not api_key:
            st.sidebar.warning("⚠️ Please enter OpenAI API key")
        elif not APIKeyManager.validate_api_key(api_key):
            st.sidebar.error("❌ Invalid API key format")
        else:
            st.sidebar.success("✅ API key entered successfully")


def main() -> None:
    """Main function to run the API key configuration page."""
    
    # Initialize UI
    ui = StreamlitUI()
    ui.setup_page()
    
    # Get API key input
    api_key = ui.render_api_key_input()
    
    # Show feedback
    ui.show_feedback(api_key)
    
    # Handle submission
    if st.button("Submit", use_container_width=True):
        if api_key and APIKeyManager.validate_api_key(api_key):
            APIKeyManager.save_api_key(api_key)
            time.sleep(1.5)  # TODO: Consider removing or replacing with proper loading state
            switch_page('upload pdf')
    
    # Render sidebar
    sidebar_stuff1()


if __name__ == "__main__":
    main()