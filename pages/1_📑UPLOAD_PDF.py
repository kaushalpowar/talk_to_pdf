"""
PDF Upload and Processing Page

This module handles the PDF document upload and processing functionality using
Streamlit interface. It allows users to select AI models, configure parameters,
and process PDF documents for analysis.
"""

import os
from typing import List, Optional
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
SUPPORTED_MODELS = ["gpt-3.5-turbo", "gpt-4"]
DEFAULT_TEMPERATURE = 0.5
TEMPERATURE_MIN = 0.1
TEMPERATURE_MAX = 1.0
TEMPERATURE_STEP = 0.1

def initialize_page() -> None:
    """Initialize the page layout and sidebar."""
    sidebar_stuff2()

def configure_model_settings():
    """Configure AI model settings and parameters."""
    model_name = st.selectbox(
        "Select the model you want to use",
        options=SUPPORTED_MODELS,
        help="Choose the AI model for processing your documents"
    )
    
    temperature = st.slider(
        "Set temperature",
        min_value=TEMPERATURE_MIN,
        max_value=TEMPERATURE_MAX,
        value=DEFAULT_TEMPERATURE,
        step=TEMPERATURE_STEP,
        help="Controls randomness in model responses. Higher values increase creativity."
    )
    
    return model_name, temperature

def handle_file_upload() -> Optional[List]:
    """Handle PDF file upload functionality."""
    return st.file_uploader(
        "Unleash the power of AI to have a conversation with your PDFs "
        "and uncover new insights, all with a single upload⬇️",
        type=['pdf'],
        accept_multiple_files=True,
        help="Upload one or more PDF files to analyze"
    )

def process_uploaded_files(
    pdf_files: List,
    model_name: str,
    temperature: float
) -> None:
    """
    Process uploaded PDF files and initialize query engine.
    
    Args:
        pdf_files: List of uploaded PDF files
        model_name: Name of the selected AI model
        temperature: Temperature parameter for model responses
    """
    try:
        reader = load_document(uploaded_files=pdf_files)
        engine = query_engine(reader, model_name, temperature)
        
        # Show success message
        st.success("Documents processed successfully! You can now proceed to chat.")
        
    except Exception as e:
        st.error(f"Error processing documents: {str(e)}")
        st.info("Please try uploading your documents again.")

def main():
    """Main function to run the PDF upload page."""
    initialize_page()
    
    # Configure model settings
    model_name, temperature = configure_model_settings()
    
    # Handle file upload
    pdf_files = handle_file_upload()
    
    if pdf_files:
        process_uploaded_files(pdf_files, model_name, temperature)
    else:
        st.info("Please upload a PDF file to begin")

if __name__ == "__main__":
    main()