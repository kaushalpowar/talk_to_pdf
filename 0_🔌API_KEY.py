"""
API Key Configuration Page for Talk to PDF Application.

This module handles the OpenAI API key configuration and validation for the PDF chat application.
It provides a user interface for API key input and manages the transition to the PDF upload page
once the key is validated.
"""

import os
import time
from dataclasses import dataclass
from typing import Optional
import logging

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
SUCCESS_MESSAGE = "✅ API key entered successfully"
WARNING_MESSAGE = "⚠️ Please enter OpenAI API key"
API_KEY_PROMPT = "Enter your OpenAI API key (https://platform.openai.com/account/api-keys)"
TRANSITION_DELAY = 1.5

@dataclass
class AppConfig:
    """Configuration settings for the application."""
    title: str = "Talk to your PDF 🤖 📑️"
    layout: str = "wide"
    api_key: Optional[str] = None

def initialize_page(config: AppConfig) -> None:
    """Initialize the Streamlit page with basic configuration.
    
    Args:
        config: AppConfig instance containing page configuration
    """
    st.set_page_config(
        page_title=PAGE_TITLE,
        page_icon=PAGE_ICON,
        layout=config.layout
    )
    st.title(config.title)

def validate_api_key(api_key: str) -> bool:
    """Validate the provided OpenAI API key.
    
    Args:
        api_key: OpenAI API key to validate
    
    Returns:
        bool: True if key is valid, False otherwise
    """
    if not api_key:
        return False
    
    try:
        # TODO: Implement proper API key validation
        # Currently just checking if key is not empty
        return True
    except Exception as e:
        logger.error(f"API key validation error: {e}")
        return False

def handle_api_key_submission(api_key: str) -> None:
    """Handle the API key submission and state transitions.
    
    Args:
        api_key: Submitted OpenAI API key
    """
    if validate_api_key(api_key):
        openai.api_key = api_key
        st.sidebar.success(SUCCESS_MESSAGE)
        time.sleep(TRANSITION_DELAY)
        switch_page('upload pdf')
    else:
        st.sidebar.warning(WARNING_MESSAGE)

def render_api_key_input() -> None:
    """Render the API key input form and handle submission."""
    st.write("#### Enter your OpenAI api key below :")
    
    api_key = st.text_input(
        API_KEY_PROMPT,
        type="password",
        key="api_key_input"
    )
    
    # Store API key in session state
    st.session_state['api_key'] = api_key

    # Show warning if no API key is provided
    if not api_key:
        st.sidebar.warning(WARNING_MESSAGE)
    
    # Handle form submission
    if st.button("Submit", use_container_width=True):
        handle_api_key_submission(api_key)

def main():
    """Main function to run the API key configuration page."""
    try:
        # Initialize application configuration
        config = AppConfig()
        
        # Setup page
        initialize_page(config)
        
        # Render API key input form
        render_api_key_input()
        
        # Add sidebar content
        sidebar_stuff1()
        
    except Exception as e:
        logger.error(f"Application error: {e}")
        st.error("An error occurred. Please try again or contact support.")

if __name__ == "__main__":
    main()