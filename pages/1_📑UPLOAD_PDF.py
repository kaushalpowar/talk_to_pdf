"""
PDF Upload and Processing Page

This module handles the PDF document upload and processing functionality using Streamlit.
It allows users to select an AI model, configure temperature settings, and upload PDF files
for processing.
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
    """Configuration settings for the AI model."""
    model_name: str
    temperature: float

def initialize_page() -> None:
    """Initialize the page layout and sidebar."""
    sidebar_stuff2()

def get_model_config() -> ModelConfig:
    """Get model configuration from user input.
    
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

def handle_pdf_upload(config: ModelConfig) -> None:
    """Handle PDF file upload and processing.
    
    Args:
        config: ModelConfig object containing model settings
    """
    pdf_files = st.file_uploader(
        "Unleash the power of AI to have a conversation with your PDFs "
        "and uncover new insights, all with a single upload⬇️",
        type=['pdf'],
        accept_multiple_files=True,
        help="Upload one or more PDF files to analyze"
    )
    
    if not pdf_files:
        st.error("Please upload a PDF file")
        return
        
    try:
        logger.info(f"Processing {len(pdf_files)} PDF files")
        reader = load_document(uploaded_files=pdf_files)
        query_engine(
            reader,
            model_name=config.model_name,
            temperature=config.temperature
        )
        
    except Exception as e:
        logger.error(f"Error processing PDF files: {str(e)}")
        st.error(
            "An error occurred while processing the PDF files. "
            "Please try again or contact support."
        )

def main() -> None:
    """Main function to run the PDF upload page."""
    try:
        initialize_page()
        config = get_model_config()
        handle_pdf_upload(config)
        
    except Exception as e:
        logger.error(f"Unexpected error in main: {str(e)}")
        st.error(
            "An unexpected error occurred. Please refresh the page "
            "or contact support if the problem persists."
        )

if __name__ == "__main__":
    main()