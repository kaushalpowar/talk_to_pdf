"""
PDF Upload and Processing Page

This module handles the PDF file upload and processing functionality for the Talk to PDF application.
It provides a user interface for model selection, temperature adjustment, and PDF file upload.
"""

import os
import logging
from typing import List, Optional
from dataclasses import dataclass

import streamlit as st
from streamlit_extras.switch_page_button import switch_page

from functions import (
    sidebar_stuff2,
    query_engine,
    save_file,
    remove_file,
    load_document
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
SUPPORTED_MODELS = ["gpt-3.5-turbo", "gpt-4"]
DEFAULT_TEMPERATURE = 0.5
TEMPERATURE_MIN = 0.1
TEMPERATURE_MAX = 1.0
TEMPERATURE_STEP = 0.1

@dataclass
class ModelConfig:
    """Configuration class for the AI model settings."""
    model_name: str
    temperature: float

def initialize_page() -> None:
    """Initialize the page layout and sidebar."""
    sidebar_stuff2()

def get_model_settings() -> ModelConfig:
    """
    Get user-selected model settings.
    
    Returns:
        ModelConfig: Selected model name and temperature settings
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
        help="Controls randomness in the model's output. Higher values make the output more diverse."
    )
    
    return ModelConfig(model_name=model_name, temperature=temperature)

def handle_file_upload() -> Optional[List]:
    """
    Handle PDF file upload functionality.
    
    Returns:
        Optional[List]: List of uploaded files if successful, None otherwise
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
    model_config: ModelConfig
) -> None:
    """
    Process uploaded PDF files and initialize the query engine.
    
    Args:
        pdf_files: List of uploaded PDF files
        model_config: Model configuration settings
    """
    try:
        reader = load_document(uploaded_files=pdf_files)
        query_engine(
            reader,
            model_config.model_name,
            model_config.temperature
        )
        logger.info(f"Successfully processed {len(pdf_files)} PDF files")
        
    except Exception as e:
        logger.error(f"Error processing PDF files: {str(e)}")
        st.error(f"Error processing PDF files: {str(e)}")

def main():
    """Main function to run the PDF upload page."""
    try:
        # Initialize page
        initialize_page()
        
        # Get model settings
        model_config = get_model_settings()
        
        # Handle file upload
        pdf_files = handle_file_upload()
        
        # Process files if uploaded
        if pdf_files:
            process_uploaded_files(pdf_files, model_config)
        else:
            st.info("Please upload a PDF file to begin")
            
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        st.error("An unexpected error occurred. Please try again or contact support.")

if __name__ == "__main__":
    main()