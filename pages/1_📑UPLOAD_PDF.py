"""
PDF Upload and Processing Page

This module handles the PDF upload functionality of the Talk to PDF application,
including model selection, temperature configuration, and document processing.
"""

import os
from typing import List, Optional
import tempfile
import logging
from dataclasses import dataclass

import streamlit as st
from streamlit_extras.switch_page_button import switch_page

from functions import (
    sidebar_stuff2,
    query_engine,
    load_document,
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
    """Configuration class for model settings."""
    model_name: str
    temperature: float

def initialize_page() -> None:
    """Initialize the page layout and sidebar."""
    sidebar_stuff2()

def get_model_configuration() -> ModelConfig:
    """
    Get model configuration from user input.
    
    Returns:
        ModelConfig: Selected model name and temperature settings
    """
    model_name = st.selectbox(
        "Select the model you want to use",
        options=SUPPORTED_MODELS,
        help="Choose between different GPT models for processing"
    )
    
    temperature = st.slider(
        "Set temperature",
        min_value=TEMPERATURE_MIN,
        max_value=TEMPERATURE_MAX,
        value=DEFAULT_TEMPERATURE,
        step=TEMPERATURE_STEP,
        help="Controls randomness in model responses. Higher values increase creativity."
    )
    
    return ModelConfig(model_name=model_name, temperature=temperature)

def handle_pdf_upload() -> Optional[List]:
    """
    Handle PDF file upload process.
    
    Returns:
        Optional[List]: Processed document if upload successful, None otherwise
    """
    uploaded_files = st.file_uploader(
        "Unleash the power of AI to have a conversation with your PDFs "
        "and uncover new insights, all with a single upload⬇️",
        type=['pdf'],
        accept_multiple_files=True,
        help="Upload one or more PDF files to analyze"
    )
    
    if not uploaded_files:
        return None
        
    try:
        logger.info(f"Processing {len(uploaded_files)} PDF files")
        return load_document(uploaded_files=uploaded_files)
    except Exception as e:
        logger.error(f"Error processing PDF files: {str(e)}")
        st.error(f"Error processing PDF files: {str(e)}")
        return None

def main() -> None:
    """Main function to run the PDF upload page."""
    try:
        initialize_page()
        
        # Get model configuration
        model_config = get_model_configuration()
        
        # Handle PDF upload
        processed_docs = handle_pdf_upload()
        
        if processed_docs:
            try:
                # Initialize query engine with processed documents
                query_engine(
                    docs=processed_docs,
                    model_name=model_config.model_name,
                    temperature=model_config.temperature
                )
            except Exception as e:
                logger.error(f"Error initializing query engine: {str(e)}")
                st.error("Failed to initialize document processing. Please try again.")
        else:
            st.error("Please upload a PDF file")
            
    except Exception as e:
        logger.error(f"Unexpected error in main function: {str(e)}")
        st.error("An unexpected error occurred. Please try again or contact support.")

if __name__ == "__main__":
    main()