"""
PDF Upload and Processing Page

This module handles the PDF document upload and processing functionality for the Talk to PDF application.
It configures the AI model settings and processes uploaded PDFs for question-answering capabilities.
"""

import os
from typing import List, Optional, Tuple
import tempfile

import streamlit as st
from streamlit_extras.switch_page_button import switch_page

from functions import sidebar_stuff2, query_engine, save_file, remove_file, load_document

# Constants
DEFAULT_TEMPERATURE = 0.5
SUPPORTED_MODELS = ["gpt-3.5-turbo", "gpt-4"]
TEMPERATURE_RANGE = (0.1, 1.0)
TEMPERATURE_STEP = 0.1

def initialize_page() -> None:
    """Initialize the page layout and sidebar."""
    sidebar_stuff2()

def get_model_settings() -> Tuple[str, float]:
    """
    Configure and get the AI model settings from user input.
    
    Returns:
        Tuple[str, float]: Selected model name and temperature setting
    """
    model_name = st.selectbox(
        "Select the model you want to use",
        options=SUPPORTED_MODELS,
        help="Choose between GPT-3.5 Turbo (faster) or GPT-4 (more capable)"
    )
    
    temperature = st.slider(
        "Set temperature",
        min_value=TEMPERATURE_RANGE[0],
        max_value=TEMPERATURE_RANGE[1],
        value=DEFAULT_TEMPERATURE,
        step=TEMPERATURE_STEP,
        help="Higher values make output more creative, lower values make it more focused"
    )
    
    return model_name, temperature

def handle_pdf_upload() -> Optional[List]:
    """
    Handle PDF file upload and processing.
    
    Returns:
        Optional[List]: Processed document reader if successful, None otherwise
    """
    pdf_files = st.file_uploader(
        "Unleash the power of AI to have a conversation with your PDFs "
        "and uncover new insights, all with a single upload⬇️",
        type=['pdf'],
        accept_multiple_files=True,
        help="Upload one or more PDF files to analyze"
    )
    
    if not pdf_files:
        st.error("Please upload a PDF file")
        return None
    
    try:
        reader = load_document(uploaded_files=pdf_files)
        return reader
    except Exception as e:
        st.error(f"Error processing PDF: {str(e)}")
        return None

def main():
    """Main function to run the PDF upload and processing page."""
    initialize_page()
    
    # Get model configuration
    model_name, temperature = get_model_settings()
    
    # Handle PDF upload and processing
    reader = handle_pdf_upload()
    
    if reader:
        try:
            # Initialize query engine with processed documents
            query_engine(reader, model_name, temperature)
            
            # TODO: Add progress indicator for document processing
            # TODO: Add validation for maximum file size and number of files
            
        except Exception as e:
            st.error(f"Error initializing query engine: {str(e)}")
            st.info("Please try again or contact support if the issue persists")

if __name__ == "__main__":
    main()