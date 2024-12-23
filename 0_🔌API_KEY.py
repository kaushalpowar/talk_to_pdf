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

# Configuration constants
PAGE_TITLE = "Talk to PDF"
PAGE_ICON = ":robot_face:"
API_KEY_URL = "https://platform.openai.com/account/api-keys"

def initialize_page_config() -> None:
    """Initialize Streamlit page configuration with consistent styling."""
    st.set_page_config(
        page_title=PAGE_TITLE,
        page_icon=PAGE_ICON,
        layout="wide"
    )
    st.title("Talk to your PDF 🤖 📑️")

def validate_api_key(api_key: str) -> bool:
    """
    Validate the provided OpenAI API key.

    Args:
        api_key: The API key to validate

    Returns:
        bool: True if the key is valid, False otherwise
    """
    if not api_key or not api_key.startswith('sk-'):
        return False
    
    try:
        # Set the API key temporarily for validation
        openai.api_key = api_key
        # TODO: Implement a lightweight API call to validate the key
        return True
    except Exception as e:
        st.error(f"Error validating API key: {str(e)}")
        return False

def handle_api_key_submission(api_key: str) -> None:
    """
    Handle the API key submission process including validation and state updates.

    Args:
        api_key: The submitted API key
    """
    if validate_api_key(api_key):
        st.session_state['api_key'] = api_key
        openai.api_key = api_key
        st.sidebar.success("✅ API key entered successfully")
        # Add small delay for better UX
        time.sleep(1.5)
        switch_page('upload pdf')
    else:
        st.sidebar.error("⚠️ Invalid API key format")

def render_api_key_input() -> Optional[str]:
    """
    Render the API key input form and handle its submission.

    Returns:
        Optional[str]: The entered API key if provided
    """
    st.write("#### Enter your OpenAI api key below :")
    api_key = st.text_input(
        f"Enter your OpenAI API key ({API_KEY_URL})",
        type="password",
        help="Your API key will be stored securely in the session state"
    )
    
    submit_button = st.button(
        "Submit",
        use_container_width=True,
        help="Click to validate and save your API key"
    )

    if submit_button and api_key:
        handle_api_key_submission(api_key)
    
    return api_key

def main() -> None:
    """Main application entry point."""
    # Initialize page configuration
    initialize_page_config()
    
    # Render API key input form
    api_key = render_api_key_input()
    
    # Show warning if no API key is provided
    if not api_key:
        st.sidebar.warning("⚠️ Please enter OpenAI API key")
    
    # Render sidebar content
    sidebar_stuff1()

if __name__ == "__main__":
    main()