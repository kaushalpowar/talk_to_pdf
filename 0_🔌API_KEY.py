"""
API Key Configuration Page for Talk to PDF Application

This module handles the OpenAI API key configuration and validation for the Talk to PDF application.
It provides a user interface for API key input and manages the transition to the PDF upload page.
"""

import logging
from typing import Optional
import time
import openai
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from functions import sidebar_stuff1

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
PAGE_TITLE = "Talk to PDF"
PAGE_ICON = ":robot_face:"
API_KEY_URL = "https://platform.openai.com/account/api-keys"

class APIKeyManager:
    """Manages OpenAI API key validation and storage."""
    
    @staticmethod
    def validate_api_key(api_key: str) -> bool:
        """
        Validates the provided OpenAI API key format.
        
        Args:
            api_key: The API key to validate
            
        Returns:
            bool: True if the key format is valid, False otherwise
        """
        if not api_key:
            return False
        # Basic format validation (can be expanded based on OpenAI's key format)
        return len(api_key.strip()) > 0

    @staticmethod
    def save_api_key(api_key: str) -> None:
        """
        Saves the API key to session state and configures OpenAI client.
        
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
    st.title("Talk to your PDF 🤖 📑️")

def render_api_key_input() -> Optional[str]:
    """
    Renders the API key input form.
    
    Returns:
        Optional[str]: The entered API key if provided
    """
    st.write("#### Enter your OpenAI api key below :")
    api_key = st.text_input(
        f"Enter your OpenAI API key ({API_KEY_URL})",
        type="password",
        help="Your API key will be stored securely in the session state"
    )
    return api_key

def main() -> None:
    """Main function to run the API key configuration page."""
    try:
        initialize_page()
        api_key = render_api_key_input()
        
        # Handle API key validation and storage
        if not api_key:
            st.sidebar.warning("⚠️ Please enter OpenAI API key")
        else:
            APIKeyManager.save_api_key(api_key)
        
        # Handle form submission
        if st.button("Submit", use_container_width=True):
            if APIKeyManager.validate_api_key(api_key):
                st.sidebar.success("✅ API key entered successfully")
                time.sleep(1.5)  # TODO: Consider removing sleep and using proper state management
                switch_page('upload pdf')
            else:
                st.error("Invalid API key format. Please check your input.")
        
        # Render sidebar content
        sidebar_stuff1()
        
    except Exception as e:
        logger.error(f"Error in API key configuration: {str(e)}")
        st.error("An error occurred while configuring the API key. Please try again.")

if __name__ == "__main__":
    main()