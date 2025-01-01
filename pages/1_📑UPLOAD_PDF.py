"""
PDF Upload and Processing Page

This module handles the PDF file upload interface and model configuration for the Talk to PDF application.
It provides users with options to select AI models and configure processing parameters before uploading
their PDF documents for analysis.
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

def configure_model_settings() -> Tuple[str, float]:
    """
    Configure AI model settings through user interface.
    
    Returns:
        Tuple[str, float]: Selected model name and temperature setting
    """
    model_name = st.selectbox(
        "Select the model you want to use",
        options=SUPPORTED_MODELS,
        help="Choose between different GPT models for processing your document"
    )
    
    temperature = st.slider(
        "Set temperature",
        min_value=TEMPERATURE_MIN,
        max_value=TEMPERATURE_MAX,
        value=DEFAULT_TEMPERATURE,
        step=TEMPERATURE_STEP,
        help="Controls randomness in the model's responses. Higher values make the output more creative but less focused."
    )
    
    return model_name, temperature

def handle_file_upload() -> Optional[List]:
    """
    Handle PDF file upload through Streamlit interface.
    
    Returns:
        Optional[List]: List of uploaded documents if successful, None otherwise
    """
    pdf_files = st.file_uploader(
        "Unleash the power of AI to have a conversation with your PDFs and uncover new insights, "
        "all with a single upload⬇️",
        type=['pdf'],
        accept_multiple_files=True,
        help="Upload one or more PDF files to analyze"
    )
    
    return pdf_files

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
        temperature: Temperature setting for the model
    """
    try:
        reader = load_document(uploaded_files=pdf_files)
        query_engine(reader, model_name, temperature)
        st.success("✅ Documents processed successfully!")
        
    except Exception as e:
        st.error(f"Error processing documents: {str(e)}")
        st.info("Please try uploading your documents again or contact support if the issue persists.")

def main():
    """Main function to run the PDF upload page."""
    initialize_page()
    
    # Configure model settings
    model_name, temperature = configure_model_settings()
    
    # Handle file upload
    pdf_files = handle_file_upload()
    
    # Process files if uploaded
    if pdf_files:
        process_uploaded_files(pdf_files, model_name, temperature)
    else:
        st.info("Please upload a PDF file to begin analysis")

if __name__ == "__main__":
    main()