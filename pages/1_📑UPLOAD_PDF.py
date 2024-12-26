"""
PDF Upload Page - Talk to PDF Application

This module handles the PDF document upload functionality and model configuration
for the Talk to PDF application. It allows users to select AI models, configure
temperature settings, and upload PDF documents for analysis.
"""

import os
from typing import List, Optional, Tuple
import tempfile

import streamlit as st
from streamlit_extras.switch_page_button import switch_page

from functions import sidebar_stuff2, query_engine, save_file, remove_file, load_document

# Constants
AVAILABLE_MODELS = {
    "gpt-3.5-turbo": "GPT-3.5 Turbo (Faster, more economical)",
    "gpt-4": "GPT-4 (More capable, better comprehension)"
}
DEFAULT_TEMPERATURE = 0.5
MIN_TEMPERATURE = 0.1
MAX_TEMPERATURE = 1.0
TEMPERATURE_STEP = 0.1

def initialize_page() -> None:
    """Initialize the page layout and sidebar."""
    sidebar_stuff2()

def setup_model_configuration() -> Tuple[str, float]:
    """
    Set up the model selection and temperature configuration UI.
    
    Returns:
        Tuple[str, float]: Selected model name and temperature value
    """
    model_name = st.selectbox(
        "Select the AI model",
        options=list(AVAILABLE_MODELS.keys()),
        format_func=lambda x: AVAILABLE_MODELS[x],
        help="Choose between different AI models based on your needs"
    )
    
    temperature = st.slider(
        "Set temperature (controls response creativity)",
        min_value=MIN_TEMPERATURE,
        max_value=MAX_TEMPERATURE,
        value=DEFAULT_TEMPERATURE,
        step=TEMPERATURE_STEP,
        help="Higher values make responses more creative, lower values make them more focused"
    )
    
    return model_name, temperature

def handle_file_upload() -> Optional[List]:
    """
    Handle PDF file upload functionality.
    
    Returns:
        Optional[List]: List of uploaded PDF files or None if no files uploaded
    """
    upload_text = (
        "Unleash the power of AI to have a conversation with your PDFs "
        "and uncover new insights, all with a single upload⬇️"
    )
    
    pdf_files = st.file_uploader(
        upload_text,
        type=['pdf'],
        accept_multiple_files=True,
        help="Upload one or more PDF files to analyze"
    )
    
    return pdf_files if pdf_files else None

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
        temperature: Temperature setting for AI responses
    """
    try:
        reader = load_document(uploaded_files=pdf_files)
        query_engine(reader, model_name, temperature)
    except Exception as e:
        st.error(f"Error processing PDF files: {str(e)}")
        st.stop()

def main():
    """Main function to run the PDF upload page."""
    initialize_page()
    
    # Setup model configuration
    model_name, temperature = setup_model_configuration()
    
    # Handle file upload
    pdf_files = handle_file_upload()
    
    # Process uploaded files
    if pdf_files:
        process_uploaded_files(pdf_files, model_name, temperature)
    else:
        st.error("Please upload a PDF file")

if __name__ == "__main__":
    main()