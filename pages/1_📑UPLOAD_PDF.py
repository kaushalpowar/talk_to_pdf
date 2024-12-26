"""
PDF Upload and Processing Page

This module handles the PDF document upload and initial processing configuration
for the Talk to PDF application. It allows users to select AI models and upload
PDF files for processing.
"""

import os
from typing import List, Optional
import logging
import tempfile

import streamlit as st
from streamlit_extras.switch_page_button import switch_page

from functions import (
    sidebar_stuff2,
    query_engine,
    load_document
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
SUPPORTED_MODELS = {
    "gpt-3.5-turbo": "GPT-3.5 Turbo",
    "gpt-4": "GPT-4"
}
DEFAULT_TEMPERATURE = 0.5
TEMPERATURE_MIN = 0.1
TEMPERATURE_MAX = 1.0
TEMPERATURE_STEP = 0.1

def initialize_page() -> None:
    """Initialize the page with sidebar and main content."""
    sidebar_stuff2()

def setup_model_configuration() -> tuple[str, float]:
    """
    Set up the model selection and temperature configuration.
    
    Returns:
        tuple: Selected model name and temperature value
    """
    model_name = st.selectbox(
        "Select the model you want to use",
        options=list(SUPPORTED_MODELS.keys()),
        format_func=lambda x: SUPPORTED_MODELS[x]
    )
    
    temperature = st.slider(
        "Set temperature",
        min_value=TEMPERATURE_MIN,
        max_value=TEMPERATURE_MAX,
        value=DEFAULT_TEMPERATURE,
        step=TEMPERATURE_STEP,
        help="Controls randomness in the model's output. Higher values make the output more diverse."
    )
    
    return model_name, temperature

def handle_pdf_upload() -> Optional[List]:
    """
    Handle PDF file upload and validation.
    
    Returns:
        Optional[List]: List of uploaded PDF files if successful, None otherwise
    """
    pdf_files = st.file_uploader(
        "Unleash the power of AI to have a conversation with your PDFs "
        "and uncover new insights, all with a single upload⬇️",
        type=['pdf'],
        accept_multiple_files=True
    )
    
    if not pdf_files:
        st.error("Please upload a PDF file")
        return None
        
    return pdf_files

def process_uploaded_files(
    pdf_files: List,
    model_name: str,
    temperature: float
) -> None:
    """
    Process uploaded PDF files and initialize the query engine.
    
    Args:
        pdf_files: List of uploaded PDF files
        model_name: Name of the selected AI model
        temperature: Temperature setting for the model
    """
    try:
        reader = load_document(uploaded_files=pdf_files)
        if not reader:
            st.error("Failed to process PDF files. Please try again.")
            return
            
        engine = query_engine(reader, model_name, temperature)
        if not engine:
            st.error("Failed to initialize query engine. Please check your configuration.")
            return
            
        logger.info(f"Successfully processed {len(pdf_files)} PDF files")
        
    except Exception as e:
        logger.error(f"Error processing PDF files: {str(e)}")
        st.error("An error occurred while processing your files. Please try again.")

def main() -> None:
    """Main function to run the PDF upload page."""
    initialize_page()
    
    model_name, temperature = setup_model_configuration()
    pdf_files = handle_pdf_upload()
    
    if pdf_files:
        process_uploaded_files(pdf_files, model_name, temperature)

if __name__ == "__main__":
    main()