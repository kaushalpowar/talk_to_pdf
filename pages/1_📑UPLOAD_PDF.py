"""
PDF Upload and Model Configuration Page

This module handles the PDF file upload interface and model configuration settings
for the Talk to PDF application. It provides users with options to select the AI model,
adjust temperature settings, and upload PDF files for processing.
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
MIN_TEMPERATURE = 0.1
MAX_TEMPERATURE = 1.0
TEMPERATURE_STEP = 0.1

def initialize_page() -> None:
    """Initialize the page layout and sidebar."""
    sidebar_stuff2()

def configure_model_settings() -> tuple[str, float]:
    """
    Configure the AI model settings through the UI.
    
    Returns:
        tuple: Selected model name and temperature setting
    """
    model_name = st.selectbox(
        "Select the model you want to use",
        options=SUPPORTED_MODELS,
        help="Choose between different GPT models for processing your documents"
    )
    
    temperature = st.slider(
        "Set temperature",
        min_value=MIN_TEMPERATURE,
        max_value=MAX_TEMPERATURE,
        value=DEFAULT_TEMPERATURE,
        step=TEMPERATURE_STEP,
        help="Controls the randomness of the model's responses"
    )
    
    return model_name, temperature

def handle_file_upload() -> Optional[List]:
    """
    Handle PDF file upload through Streamlit's file uploader.
    
    Returns:
        Optional[List]: List of uploaded files or None if no files uploaded
    """
    pdf_files = st.file_uploader(
        "Unleash the power of AI to have a conversation with your PDFs "
        "and uncover new insights, all with a single upload⬇️",
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
    Process the uploaded PDF files and initialize the query engine.
    
    Args:
        pdf_files: List of uploaded PDF files
        model_name: Selected AI model name
        temperature: Temperature setting for the model
    """
    try:
        reader = load_document(uploaded_files=pdf_files)
        query_engine(reader, model_name, temperature)
    except Exception as e:
        st.error(f"Error processing PDF files: {str(e)}")
        st.stop()

def main() -> None:
    """Main function to run the PDF upload and model configuration page."""
    initialize_page()
    
    # Configure model settings
    model_name, temperature = configure_model_settings()
    
    # Handle file upload
    pdf_files = handle_file_upload()
    
    # Process uploaded files
    if pdf_files:
        process_uploaded_files(pdf_files, model_name, temperature)
    else:
        st.error("Please upload a PDF file")

if __name__ == "__main__":
    main()