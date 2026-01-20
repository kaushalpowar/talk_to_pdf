"""
API Key Configuration Page for Talk to PDF Application

This module handles the OpenAI API key configuration and validation for the Talk to PDF
application. It provides a user interface for API key input and manages the transition
to the PDF upload page once the key is validated.
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
API_KEY_LINK = "https://platform.openai.com/account/api-keys"
SUCCESS_MESSAGE = "✅ API key entered successfully"
WARNING_MESSAGE = "⚠️ Please enter OpenAI API key"
NEXT_PAGE = "upload pdf"
DELAY_SECONDS = 1.5


class APIKeyManager:
    """Manages OpenAI API key configuration and validation."""
    
    def __init__(self):
        """Initialize the API key manager with session state."""
        self.session_state = st.session_state
        
    def setup_page(self) -> None:
        """Configure the page layout and title."""
        st.set_page_config(
            page_title="Talk to PDF",
            page_icon=PAGE_ICON,
            layout="wide"
        )
        st.title(TITLE)
        
    def get_api_key(self) -> Optional[str]:
        """
        Get API key from user input and store in session state.
        
        Returns:
            Optional[str]: The entered API key or None if not provided
        """
        st.write("#### Enter your OpenAI api key below :")
        api_key = st.text_input(
            f"Enter your OpenAI API key ({API_KEY_LINK})",
            type="password"
        )
        self.session_state['api_key'] = api_key
        return api_key
    
    def validate_api_key(self, api_key: str) -> bool:
        """
        Validate the provided API key.
        
        Args:
            api_key (str): OpenAI API key to validate
            
        Returns:
            bool: True if key is valid, False otherwise
        """
        if not api_key:
            st.sidebar.warning(WARNING_MESSAGE)
            return False
        
        try:
            openai.api_key = api_key
            # TODO: Add actual API key validation by making a test request
            return True
        except Exception as e:
            st.sidebar.error(f"Error validating API key: {str(e)}")
            return False
    
    def handle_submit(self, api_key: str) -> None:
        """
        Handle the submit button click event.
        
        Args:
            api_key (str): The API key to process
        """
        submit = st.button("Submit", use_container_width=True)
        if submit and self.validate_api_key(api_key):
            st.sidebar.success(SUCCESS_MESSAGE)
            time.sleep(DELAY_SECONDS)
            switch_page(NEXT_PAGE)


def main():
    """Main function to run the API key configuration page."""
    try:
        # Initialize API key manager
        api_manager = APIKeyManager()
        
        # Setup page configuration
        api_manager.setup_page()
        
        # Get and process API key
        api_key = api_manager.get_api_key()
        api_manager.handle_submit(api_key)
        
        # Setup sidebar
        sidebar_stuff1()
        
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        # TODO: Add proper error logging


if __name__ == "__main__":
    main()