"""
PDF Upload and Model Configuration Page

This module handles the PDF file upload interface and model configuration settings
for the Talk to PDF application. It provides a user interface for selecting the
OpenAI model, temperature settings, and uploading PDF files for processing.
"""

import os
from typing import List, Optional, Tuple
import tempfile

import streamlit as st
from streamlit_extras.switch_page_button import switch_page

from functions import (
    sidebar_stuff2,
    query_engine,
    save_file,
    remove_file,
    load_document
)

# Constants
SUPPORTED_MODELS = ("gpt-3.5-turbo", "gpt-4")
DEFAULT_TEMPERATURE = 0.5
TEMPERATURE_MIN = 0.1
TEMPERATURE_MAX = 1.0
TEMPERATURE_STEP = 0.1

def initialize_page() -> None:
    """Initialize the page layout and sidebar."""
    sidebar_stuff2()

def get_model_settings() -> Tuple[str, float]:
    """
    Get model configuration settings from user input.
    
    Returns:
        Tuple[str, float]: Selected model name and temperature setting
    """
    model_name = st.selectbox(
        "Select the model you want to use",
        options=SUPPORTED_MODELS,
        help="Choose between GPT-3.5 Turbo (faster, cheaper) or GPT-4 (more capable)"
    )
    
    temperature = st.slider(
        "Set temperature",
        min_value=TEMPERATURE_MIN,
        max_value=TEMPERATURE_MAX,
        value=DEFAULT_TEMPERATURE,
        step=TEMPERATURE_STEP,
        help="Higher values make output more creative, lower values make it more focused"
    )
    
    return model_name, temperature

def handle_file_upload() -> Optional[List]:
    """
    Handle PDF file upload process.
    
    Returns:
        Optional[List]: List of processed documents if upload successful, None otherwise
    """
    uploaded_files = st.file_uploader(
        "Unleash the power of AI to have a conversation with your PDFs "
        "and uncover new insights, all with a single upload⬇️",
        type=['pdf'],
        accept_multiple_files=True,
        help="Upload one or more PDF files to analyze"
    )
    
    if not uploaded_files:
        st.error("Please upload a PDF file")
        return None
        
    try:
        documents = load_document(uploaded_files=uploaded_files)
        return documents
    except Exception as e:
        st.error(f"Error processing PDF file: {str(e)}")
        return None

def main():
    """Main function to run the PDF upload and model configuration page."""
    initialize_page()
    
    # Get model settings
    model_name, temperature = get_model_settings()
    
    # Handle file upload
    documents = handle_file_upload()
    
    # Process documents if available
    if documents:
        try:
            # Initialize query engine with selected settings
            engine = query_engine(
                docs=documents,
                model_name=model_name,
                temperature=temperature
            )
            
            # Store engine in session state and proceed
            st.session_state['query_engine'] = engine
            
        except Exception as e:
            st.error(
                "Error initializing query engine. Please check your settings "
                f"and try again: {str(e)}"
            )

if __name__ == "__main__":
    main()