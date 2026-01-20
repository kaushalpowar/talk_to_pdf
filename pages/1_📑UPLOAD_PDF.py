"""
PDF Upload and Configuration Page

This module handles the PDF file upload interface and model configuration for the Talk to PDF application.
It provides users with options to select the AI model and configure temperature parameters before
processing PDF documents.
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

def get_model_config() -> Tuple[str, float]:
    """
    Get model configuration from user input.
    
    Returns:
        Tuple[str, float]: Selected model name and temperature value
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
        help="Controls randomness in the model's output. Higher values (1.0) make output more diverse, "
             "lower values (0.1) make it more focused."
    )
    
    return model_name, temperature

def handle_pdf_upload() -> Optional[List]:
    """
    Handle PDF file upload process.
    
    Returns:
        Optional[List]: Loaded document if successful, None otherwise
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
        return load_document(uploaded_files=pdf_files)
    except Exception as e:
        st.error(f"Error processing PDF file: {str(e)}")
        return None

def main():
    """Main function to run the PDF upload page."""
    initialize_page()
    
    # Get model configuration
    model_name, temperature = get_model_config()
    
    # Handle PDF upload
    documents = handle_pdf_upload()
    
    if documents:
        try:
            # Process documents and create query engine
            engine = query_engine(documents, model_name, temperature)
            
            # Store engine in session state (handled by query_engine function)
            # The function automatically switches to chat page on success
            
        except Exception as e:
            st.error(
                "An error occurred while processing the document. "
                f"Please try again. Error: {str(e)}"
            )
    else:
        st.error("Please upload a PDF file")

if __name__ == "__main__":
    main()