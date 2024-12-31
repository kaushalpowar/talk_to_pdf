"""
PDF Upload and Processing Page

This module handles the PDF document upload and processing functionality for the Talk to PDF application.
It provides a user interface for model selection, temperature adjustment, and PDF file upload.
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
DEFAULT_TEMPERATURE = 0.5
TEMPERATURE_MIN = 0.1
TEMPERATURE_MAX = 1.0
TEMPERATURE_STEP = 0.1
SUPPORTED_MODELS = ["gpt-3.5-turbo", "gpt-4"]

def initialize_page() -> None:
    """Initialize the page layout and sidebar."""
    sidebar_stuff2()

def setup_model_selection() -> tuple[str, float]:
    """
    Set up the model selection and temperature adjustment UI components.
    
    Returns:
        tuple[str, float]: Selected model name and temperature value
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
        help="Controls response creativity: Lower values (0.1) for focused responses, "
             "higher values (1.0) for more creative outputs"
    )
    
    return model_name, temperature

def handle_pdf_upload() -> None:
    """Handle PDF file upload and processing."""
    pdf_files = st.file_uploader(
        "Unleash the power of AI to have a conversation with your PDFs "
        "and uncover new insights, all with a single upload ⬇️",
        type=['pdf'],
        accept_multiple_files=True,
        help="Upload one or more PDF files to analyze"
    )
    
    if not pdf_files:
        st.error("Please upload a PDF file")
        return
    
    try:
        with st.spinner("Processing PDF documents..."):
            documents = load_document(uploaded_files=pdf_files)
            model_name, temperature = setup_model_selection()
            query_engine(documents, model_name, temperature)
            
    except Exception as e:
        st.error(f"Error processing PDF: {str(e)}")
        st.info("Please try uploading the file again or contact support if the issue persists.")

def main() -> None:
    """Main function to run the PDF upload page."""
    initialize_page()
    handle_pdf_upload()

if __name__ == "__main__":
    main()