"""
API Key Configuration Page for Talk to PDF Application.

This module handles the OpenAI API key setup and validation for the PDF chat application.
It provides a user interface for API key input and manages the transition to the PDF upload page.
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

def setup_page_config() -> None:
    """Configure the Streamlit page settings."""
    st.set_page_config(
        page_title="Talk to PDF",
        page_icon=PAGE_ICON,
        layout="wide"
    )
    st.title(TITLE)

def validate_api_key(api_key: str) -> bool:
    """
    Validate the provided OpenAI API key.

    Args:
        api_key (str): The API key to validate

    Returns:
        bool: True if the key is not empty, False otherwise
    """
    return bool(api_key and api_key.strip())

def handle_api_key_submission(api_key: str) -> None:
    """
    Handle the API key submission and state updates.

    Args:
        api_key (str): The submitted API key
    """
    if validate_api_key(api_key):
        openai.api_key = api_key
        st.sidebar.success(SUCCESS_MESSAGE)
        time.sleep(TRANSITION_DELAY)
        switch_page(NEXT_PAGE)
    else:
        st.sidebar.warning(WARNING_MESSAGE)

def render_api_key_input() -> Optional[str]:
    """
    Render the API key input field and return the entered value.

    Returns:
        Optional[str]: The entered API key or None
    """
    st.write("#### Enter your OpenAI api key below :")
    api_key = st.text_input(
        API_KEY_PLACEHOLDER,
        type="password",
        key="api_key_input"
    )
    return api_key

def main() -> None:
    """Main function to run the API key configuration page."""
    setup_page_config()
    
    # Render API key input
    api_key = render_api_key_input()
    
    # Store API key in session state
    st.session_state['api_key'] = api_key
    
    # Handle empty API key
    if not api_key:
        st.sidebar.warning(WARNING_MESSAGE)
    else:
        openai.api_key = api_key
    
    # Handle submit button
    if st.button("Submit", use_container_width=True):
        handle_api_key_submission(api_key)
    
    # Render sidebar content
    sidebar_stuff1()

if __name__ == "__main__":
    main()