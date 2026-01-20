"""
API Key Configuration Page for Talk to PDF Application

This module handles the OpenAI API key configuration and validation for the Talk to PDF application.
It provides a user interface for API key input and manages the transition to the PDF upload page
upon successful configuration.
"""

import os
import time
from typing import Optional

import openai
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, ServiceContext
from llama_index.llms.openai import OpenAI

from functions import sidebar_stuff1

class APIKeyConfig:
    """Manages OpenAI API key configuration and validation."""
    
    def __init__(self):
        """Initialize API key configuration."""
        self.api_key: Optional[str] = os.getenv('OPENAI_API_KEY')
        
    def validate_api_key(self, api_key: str) -> bool:
        """
        Validate the provided OpenAI API key format.
        
        Args:
            api_key: The API key to validate
            
        Returns:
            bool: True if key format is valid, False otherwise
        """
        if not api_key:
            return False
        # Basic format validation for OpenAI API keys
        return api_key.startswith('sk-') and len(api_key) > 20
    
    def set_api_key(self, api_key: str) -> None:
        """
        Set the OpenAI API key for use in the application.
        
        Args:
            api_key: The API key to set
        """
        self.api_key = api_key
        openai.api_key = api_key
        st.session_state['api_key'] = api_key

def setup_page():
    """Configure the Streamlit page settings."""
    st.set_page_config(
        page_title="Talk to PDF",
        page_icon=":robot_face:",
        layout="wide"
    )
    st.title("Talk to your PDF 🤖 📑️")

def render_api_key_input(config: APIKeyConfig) -> None:
    """
    Render the API key input form and handle submission.
    
    Args:
        config: APIKeyConfig instance for managing API key
    """
    st.write("#### Enter your OpenAI API key below:")
    
    api_key = st.text_input(
        "Enter your OpenAI API key (https://platform.openai.com/account/api-keys)",
        type="password",
        help="Your API key will be stored securely in the session state"
    )
    
    if not api_key:
        st.sidebar.warning("⚠️ Please enter OpenAI API key")
    elif not config.validate_api_key(api_key):
        st.sidebar.error("❌ Invalid API key format")
    else:
        config.set_api_key(api_key)
        st.sidebar.success("✅ API key validated")
    
    submit = st.button("Submit", use_container_width=True)
    
    if submit:
        if config.validate_api_key(api_key):
            st.sidebar.success("✅ API key configured successfully")
            time.sleep(1.5)
            switch_page('upload pdf')
        else:
            st.error("Please enter a valid OpenAI API key")

def main():
    """Main application entry point."""
    try:
        setup_page()
        config = APIKeyConfig()
        render_api_key_input(config)
        sidebar_stuff1()
        
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.info("Please refresh the page and try again")

if __name__ == "__main__":
    main()