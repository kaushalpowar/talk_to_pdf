"""
PDF Upload and Processing Page

This module handles the PDF document upload functionality and model configuration
for the Talk to PDF application. It provides a user interface for selecting AI models,
adjusting temperature settings, and uploading PDF documents for processing.
"""

import os
from typing import List, Optional, Tuple
import tempfile
import logging
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
SUPPORTED_MODELS = {
    "gpt-3.5-turbo": "GPT-3.5 Turbo (Faster, more economical)",
    "gpt-4": "GPT-4 (More capable, better reasoning)"
}
DEFAULT_TEMPERATURE = 0.5
TEMPERATURE_MIN = 0.1
TEMPERATURE_MAX = 1.0
TEMPERATURE_STEP = 0.1

@dataclass
class ModelConfig:
    """Configuration class for AI model settings."""
    model_name: str
    temperature: float

def initialize_page() -> None:
    """Initialize the page layout and sidebar."""
    sidebar_stuff2()

def get_model_settings() -> ModelConfig:
    """
    Get model settings from user input.
    
    Returns:
        ModelConfig: Selected model configuration
    """
    model_name = st.selectbox(
        "Select the model you want to use",
        options=list(SUPPORTED_MODELS.keys()),
        help="Choose between different GPT models based on your needs"
    )
    
    temperature = st.slider(
        "Set temperature",
        min_value=TEMPERATURE_MIN,
        max_value=TEMPERATURE_MAX,
        value=DEFAULT_TEMPERATURE,
        step=TEMPERATURE_STEP,
        help="Controls randomness in responses. Higher values make output more creative but less focused."
    )
    
    return ModelConfig(model_name=model_name, temperature=temperature)

def handle_file_upload() -> Optional[List]:
    """
    Handle PDF file upload process.
    
    Returns:
        Optional[List]: List of processed documents if successful, None otherwise
    """
    uploaded_files = st.file_uploader(
        "Unleash the power of AI to have a conversation with your PDFs and uncover new insights, all with a single upload⬇️",
        type=['pdf'],
        accept_multiple_files=True,
        help="Upload one or more PDF files to analyze"
    )
    
    if not uploaded_files:
        return None
        
    try:
        documents = load_document(uploaded_files=uploaded_files)
        logger.info(f"Successfully processed {len(uploaded_files)} PDF files")
        return documents
    except Exception as e:
        logger.error(f"Error processing PDF files: {str(e)}")
        st.error(f"Error processing PDF files: {str(e)}")
        return None

def main() -> None:
    """Main function to run the PDF upload page."""
    try:
        # Initialize page
        initialize_page()
        
        # Get model settings
        model_config = get_model_settings()
        
        # Handle file upload
        documents = handle_file_upload()
        
        if documents:
            # Process documents and create query engine
            engine = query_engine(
                docs=documents,
                model_name=model_config.model_name,
                temperature=model_config.temperature
            )
            
            if engine:
                logger.info("Successfully created query engine")
            else:
                st.error("Failed to create query engine")
        else:
            st.info("Please upload a PDF file to begin")
            
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        st.error("An unexpected error occurred. Please try again or contact support.")

if __name__ == "__main__":
    main()