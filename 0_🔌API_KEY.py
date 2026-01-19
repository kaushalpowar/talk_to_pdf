"""
API Key Configuration Module for Talk to PDF Application

This module handles the OpenAI API key configuration and validation for the Talk to PDF
application. It provides a user interface for API key input and manages the key storage
in the session state.
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
PAGE_TITLE = "Talk to PDF"
PAGE_ICON = ":robot_face:"
TITLE = "Talk to your PDF 🤖 📑️"
API_KEY_URL = "https://platform.openai.com/account/api-keys"

def initialize_page_config() -> None:
    """Initialize the Streamlit page configuration."""
    st.set_page_config(
        page_title=PAGE_TITLE,
        page_icon=PAGE_ICON,
        layout="wide"
    )

def validate_api_key(api_key: str) -> bool:
    """
    Validate the provided OpenAI API key.

    Args:
        api_key (str): The API key to validate

    Returns:
        bool: True if the key is not empty, False otherwise
    """
    return bool(api_key and api_key.strip())

def setup_api_key(api_key: str) -> None:
    """
    Configure the OpenAI API key in both session state and openai client.

    Args:
        api_key (str): The API key to configure
    """
    st.session_state['api_key'] = api_key
    openai.api_key = api_key

def render_api_key_input() -> Optional[str]:
    """
    Render the API key input field and return the entered key.

    Returns:
        Optional[str]: The entered API key or None if not provided
    """
    st.write("#### Enter your OpenAI api key below :")
    return st.text_input(
        f"Enter your OpenAI API key ({API_KEY_URL})",
        type="password",
        help="Your API key will be stored securely in the session state"
    )

def handle_api_key_submission() -> None:
    """Handle the API key submission and navigation logic."""
    submit = st.button("Submit", use_container_width=True)
    if submit:
        st.sidebar.success("✅ API key entered successfully")
        # Add small delay for better UX
        time.sleep(1.5)
        switch_page('upload pdf')

def show_api_key_warning() -> None:
    """Display a warning message when API key is missing."""
    st.sidebar.warning("⚠️ Please enter OpenAI API key")

def main() -> None:
    """Main function to run the API key configuration interface."""
    # Initialize page
    initialize_page_config()
    st.title(TITLE)

    # Get API key input
    api_key = render_api_key_input()

    # Handle API key validation and setup
    if not validate_api_key(api_key):
        show_api_key_warning()
    else:
        setup_api_key(api_key)
        handle_api_key_submission()

    # Render sidebar content
    sidebar_stuff1()

if __name__ == "__main__":
    main()