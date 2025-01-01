"""
API Key Configuration Page for Talk to PDF Application.

This module handles the OpenAI API key setup and validation, serving as the entry point
for the Talk to PDF application. It provides a user interface for API key input and
manages the transition to the PDF upload page upon successful validation.
"""

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
API_KEY_PLACEHOLDER = "Enter your OpenAI API key (https://platform.openai.com/account/api-keys)"
SUCCESS_MESSAGE = "✅ API key entered successfully"
WARNING_MESSAGE = "⚠️ Please enter OpenAI API key"
NEXT_PAGE = "upload pdf"
TRANSITION_DELAY = 1.5

class APIKeyManager:
    """Manages the OpenAI API key configuration and validation."""
    
    @staticmethod
    def initialize_session_state() -> None:
        """Initialize session state variables if they don't exist."""
        if 'api_key' not in st.session_state:
            st.session_state['api_key'] = None

    @staticmethod
    def validate_api_key(api_key: str) -> bool:
        """
        Validate the provided OpenAI API key.
        
        Args:
            api_key: The API key to validate
            
        Returns:
            bool: True if the key is not empty, False otherwise
        """
        return bool(api_key and api_key.strip())

    @staticmethod
    def configure_openai(api_key: str) -> None:
        """
        Configure OpenAI with the provided API key.
        
        Args:
            api_key: The API key to configure
        """
        openai.api_key = api_key
        st.session_state['api_key'] = api_key

class PageConfig:
    """Handles page configuration and layout."""
    
    @staticmethod
    def setup_page() -> None:
        """Configure the page layout and title."""
        st.set_page_config(
            page_title=TITLE,
            page_icon=PAGE_ICON,
            layout="wide"
        )
        st.title(TITLE)

    @staticmethod
    def render_api_key_input() -> Optional[str]:
        """
        Render the API key input field.
        
        Returns:
            Optional[str]: The entered API key or None
        """
        st.write("#### Enter your OpenAI api key below :")
        return st.text_input(
            API_KEY_PLACEHOLDER,
            type="password"
        )

    @staticmethod
    def handle_submission(api_key: str) -> None:
        """
        Handle the API key submission process.
        
        Args:
            api_key: The submitted API key
        """
        submit = st.button("Submit", use_container_width=True)
        
        if submit:
            st.sidebar.success(SUCCESS_MESSAGE)
            time.sleep(TRANSITION_DELAY)
            switch_page(NEXT_PAGE)

def main() -> None:
    """Main application entry point."""
    # Initialize components
    api_manager = APIKeyManager()
    page_config = PageConfig()
    
    # Setup page
    page_config.setup_page()
    api_manager.initialize_session_state()
    
    # Render API key input
    api_key = page_config.render_api_key_input()
    
    # Handle API key validation
    if not api_manager.validate_api_key(api_key):
        st.sidebar.warning(WARNING_MESSAGE)
    else:
        api_manager.configure_openai(api_key)
        page_config.handle_submission(api_key)
    
    # Render sidebar
    sidebar_stuff1()

if __name__ == "__main__":
    main()