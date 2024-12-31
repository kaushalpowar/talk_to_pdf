"""
Talk to PDF - API Key Configuration Page
This module handles the OpenAI API key configuration and validation for the Talk to PDF application.
"""

import os
import time
from typing import Optional

import openai
import streamlit as st
from streamlit_extras.switch_page_button import switch_page

from functions import sidebar_stuff1

# Constants
OPENAI_API_KEY_URL = "https://platform.openai.com/account/api-keys"
PAGE_TITLE = "Talk to PDF"
PAGE_ICON = ":robot_face:"
SESSION_KEY_API = 'api_key'

def initialize_page() -> None:
    """Initialize the Streamlit page configuration and title."""
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
        bool: True if the API key is valid, False otherwise
    """
    if not api_key or len(api_key.strip()) < 20:  # Basic length validation
        return False
    
    try:
        openai.api_key = api_key
        # TODO: Add a lightweight API call to verify key validity
        return True
    except Exception as e:
        st.error(f"Error validating API key: {str(e)}")
        return False

def setup_api_key_input() -> Optional[str]:
    """
    Set up and handle the API key input interface.
    
    Returns:
        Optional[str]: The entered API key if valid, None otherwise
    """
    st.write("#### Enter your OpenAI API key below:")
    
    # Check for existing API key in environment variables
    default_key = os.getenv("OPENAI_API_KEY", "")
    
    api_key = st.text_input(
        f"Enter your OpenAI API key ({OPENAI_API_KEY_URL})",
        type="password",
        value=default_key
    )
    
    return api_key if api_key else None

def handle_submit_button(api_key: str) -> None:
    """
    Handle the submit button click event.
    
    Args:
        api_key: The API key to process
    """
    if validate_api_key(api_key):
        st.sidebar.success("✅ API key entered successfully")
        # Store API key in session state
        st.session_state[SESSION_KEY_API] = api_key
        # Add slight delay for better UX
        time.sleep(1.5)
        switch_page('upload pdf')
    else:
        st.sidebar.error("❌ Invalid API key format")

def main() -> None:
    """Main application entry point."""
    try:
        initialize_page()
        
        # Setup API key input
        api_key = setup_api_key_input()
        
        # Update session state
        st.session_state[SESSION_KEY_API] = api_key
        
        # Show warning if no API key
        if not api_key:
            st.sidebar.warning("⚠️ Please enter OpenAI API key")
        
        # Submit button
        if st.button("Submit", use_container_width=True):
            handle_submit_button(api_key)
        
        # Setup sidebar
        sidebar_stuff1()
        
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        # TODO: Add proper error logging
        
if __name__ == "__main__":
    main()