"""
PDF Upload and Processing Module

This module handles the PDF document upload and processing functionality for the Talk to PDF application.
It provides a user interface for model selection, temperature adjustment, and PDF file upload.
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

def setup_page() -> None:
    """Initialize the page layout and sidebar."""
    sidebar_stuff2()

def configure_model() -> Tuple[str, float]:
    """
    Configure the model settings through user input.
    
    Returns:
        Tuple[str, float]: Selected model name and temperature setting
    """
    model_name = st.selectbox(
        "Select the model you want to use",
        options=SUPPORTED_MODELS
    )
    
    temperature = st.slider(
        "Set temperature",
        min_value=TEMPERATURE_MIN,
        max_value=TEMPERATURE_MAX,
        value=DEFAULT_TEMPERATURE,
        step=TEMPERATURE_STEP,
        help="Controls the randomness of the model's output. Higher values make the output more diverse."
    )
    
    return model_name, temperature

def handle_file_upload() -> Optional[List]:
    """
    Handle PDF file upload and processing.
    
    Returns:
        Optional[List]: Processed document reader object if successful, None otherwise
    """
    pdf_files = st.file_uploader(
        "Unleash the power of AI to have a conversation with your PDFs "
        "and uncover new insights, all with a single upload⬇️",
        type=['pdf'],
        accept_multiple_files=True,
        help="Upload one or more PDF files to analyze"
    )
    
    if not pdf_files:
        return None
        
    try:
        reader = load_document(uploaded_files=pdf_files)
        return reader
    except Exception as e:
        st.error(f"Error processing PDF file: {str(e)}")
        return None

def main():
    """Main execution function."""
    setup_page()
    
    # Configure model settings
    model_name, temperature = configure_model()
    
    # Handle file upload
    reader = handle_file_upload()
    
    if reader:
        try:
            # Initialize query engine with selected parameters
            query_engine_instance = query_engine(
                reader,
                model_name,
                temperature
            )
            
            # Store query engine in session state
            st.session_state['query_engine'] = query_engine_instance
            
        except Exception as e:
            st.error(
                "An error occurred while processing the document. "
                f"Error: {str(e)}"
            )
    else:
        st.info("Please upload a PDF file to begin")

if __name__ == "__main__":
    main()