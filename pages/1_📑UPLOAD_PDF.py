"""
PDF Upload and Processing Page

This module handles the PDF document upload interface and model configuration
for the Talk to PDF application. It provides a user interface for selecting
AI model parameters and uploading PDF documents for processing.
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
    "gpt-3.5-turbo": "GPT-3.5 Turbo",
    "gpt-4": "GPT-4"
}
DEFAULT_TEMPERATURE = 0.5
TEMPERATURE_RANGE = (0.1, 1.0)
TEMPERATURE_STEP = 0.1

@dataclass
class ModelConfig:
    """Configuration settings for the AI model."""
    model_name: str
    temperature: float

def setup_page() -> None:
    """Initialize the page layout and sidebar."""
    sidebar_stuff2()

def validate_temperature(temp: float) -> float:
    """
    Validate and constrain temperature value within acceptable range.
    
    Args:
        temp: Input temperature value
    
    Returns:
        float: Validated temperature value
    """
    return max(TEMPERATURE_RANGE[0], min(TEMPERATURE_RANGE[1], temp))

def get_model_config() -> ModelConfig:
    """
    Get model configuration from user input.
    
    Returns:
        ModelConfig: Selected model configuration
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
        help="Controls randomness in the model's output. Higher values make the output more diverse."
    )
    
    return ModelConfig(model_name=model_name, temperature=temperature)

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
        accept_multiple_files=True
    )
    
    if not uploaded_files:
        st.error("Please upload a PDF file")
        return None
    
    try:
        logger.info(f"Processing {len(uploaded_files)} PDF files")
        document_data = load_document(uploaded_files=uploaded_files)
        return document_data
    except Exception as e:
        logger.error(f"Error processing PDF files: {str(e)}")
        st.error(f"Error processing PDF files: {str(e)}")
        return None

def main():
    """Main application flow."""
    setup_page()
    
    # Get model configuration
    model_config = get_model_config()
    
    # Handle PDF upload
    document_data = handle_pdf_upload()
    
    if document_data:
        try:
            # Initialize query engine with processed documents
            query_engine_instance = query_engine(
                document_data,
                model_config.model_name,
                model_config.temperature
            )
            
            # Store query engine in session state
            st.session_state['query_engine'] = query_engine_instance
            
            logger.info("Document processing complete, redirecting to chat interface")
        except Exception as e:
            logger.error(f"Error initializing query engine: {str(e)}")
            st.error("An error occurred while processing your document. Please try again.")

if __name__ == "__main__":
    main()