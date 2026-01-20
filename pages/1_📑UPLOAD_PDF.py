"""
PDF Upload and Model Configuration Page

This module handles the PDF file upload interface and model configuration settings
for the Talk to PDF application. It provides users with options to select the AI model
and configure temperature settings before processing PDF documents.
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
SUPPORTED_MODELS = ["gpt-3.5-turbo", "gpt-4"]
DEFAULT_TEMPERATURE = 0.5
TEMPERATURE_MIN = 0.1
TEMPERATURE_MAX = 1.0
TEMPERATURE_STEP = 0.1

@dataclass
class ModelConfig:
    """Stores model configuration parameters."""
    model_name: str
    temperature: float

def initialize_page() -> None:
    """Initialize the page with sidebar and basic UI elements."""
    sidebar_stuff2()

def get_model_config() -> ModelConfig:
    """
    Get model configuration from user input.
    
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
        help="Controls randomness in the model's output. Higher values (1.0) make output more diverse, "
             "lower values (0.1) make it more focused."
    )
    
    return ModelConfig(model_name=model_name, temperature=temperature)

def handle_file_upload() -> Optional[List]:
    """
    Handle PDF file upload process.
    
    Returns:
        Optional[List]: Loaded document if successful, None otherwise
    """
    uploaded_files = st.file_uploader(
        "Unleash the power of AI to have a conversation with your PDFs "
        "and uncover new insights, all with a single upload⬇️",
        type=['pdf'],
        accept_multiple_files=True,
        help="Upload one or more PDF files to analyze"
    )
    
    if not uploaded_files:
        st.error("Please upload a PDF file")
        return None
    
    try:
        logger.info(f"Processing {len(uploaded_files)} PDF files")
        documents = load_document(uploaded_files=uploaded_files)
        return documents
    except Exception as e:
        logger.error(f"Error processing PDF files: {str(e)}")
        st.error(f"Error processing PDF files: {str(e)}")
        return None

def main() -> None:
    """Main function to run the PDF upload and model configuration page."""
    try:
        # Initialize page
        initialize_page()
        
        # Get model configuration
        model_config = get_model_config()
        
        # Handle file upload
        documents = handle_file_upload()
        
        # Process documents if available
        if documents:
            try:
                engine = query_engine(
                    docs=documents,
                    model_name=model_config.model_name,
                    temperature=model_config.temperature
                )
                logger.info("Query engine created successfully")
            except Exception as e:
                logger.error(f"Error creating query engine: {str(e)}")
                st.error("Error processing documents. Please try again.")
                
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        st.error("An unexpected error occurred. Please try again or contact support.")

if __name__ == "__main__":
    main()