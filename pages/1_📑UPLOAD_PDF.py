"""
PDF Upload and Processing Page

This module handles the PDF document upload and initial processing for the Talk to PDF application.
It configures the AI model settings and prepares documents for query processing.
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
SUPPORTED_MODELS = {
    "gpt-3.5-turbo": "GPT-3.5 Turbo",
    "gpt-4": "GPT-4"
}
DEFAULT_TEMPERATURE = 0.5
TEMPERATURE_RANGE = (0.1, 1.0)
TEMPERATURE_STEP = 0.1

def initialize_page() -> None:
    """Initialize the page layout and sidebar."""
    sidebar_stuff2()

def configure_model_settings() -> Tuple[str, float]:
    """
    Configure AI model settings through user input.
    
    Returns:
        Tuple[str, float]: Selected model name and temperature setting
    """
    model_name = st.selectbox(
        "Select the model you want to use",
        options=list(SUPPORTED_MODELS.keys()),
        format_func=lambda x: SUPPORTED_MODELS[x]
    )
    
    temperature = st.slider(
        "Set temperature",
        min_value=TEMPERATURE_RANGE[0],
        max_value=TEMPERATURE_RANGE[1],
        value=DEFAULT_TEMPERATURE,
        step=TEMPERATURE_STEP,
        help="Controls randomness in the model's responses"
    )
    
    return model_name, temperature

def handle_pdf_upload() -> Optional[List]:
    """
    Handle PDF file upload and processing.
    
    Returns:
        Optional[List]: Processed document data if successful, None otherwise
    """
    uploaded_files = st.file_uploader(
        "Unleash the power of AI to have a conversation with your PDFs and uncover new insights, "
        "all with a single upload⬇️",
        type=['pdf'],
        accept_multiple_files=True,
        help="Upload one or more PDF files to analyze"
    )
    
    if not uploaded_files:
        st.error("Please upload a PDF file")
        return None
    
    try:
        return load_document(uploaded_files=uploaded_files)
    except Exception as e:
        st.error(f"Error processing PDF: {str(e)}")
        return None

def main():
    """Main execution flow for the PDF upload page."""
    initialize_page()
    
    # Configure model settings
    model_name, temperature = configure_model_settings()
    
    # Handle PDF upload and processing
    processed_docs = handle_pdf_upload()
    
    if processed_docs:
        try:
            # Initialize query engine with processed documents
            query_engine(
                reader=processed_docs,
                model_name=model_name,
                temperature=temperature
            )
        except Exception as e:
            st.error(f"Error initializing query engine: {str(e)}")
            # TODO: Add logging for error tracking
            return

if __name__ == "__main__":
    main()