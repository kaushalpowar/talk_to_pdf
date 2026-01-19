"""
PDF Upload and Processing Page

This module handles the PDF document upload interface and initialization of the query engine
for the Talk to PDF application. It provides user controls for model selection and
temperature settings while managing document processing through LlamaIndex.
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
DEFAULT_TEMPERATURE = 0.5
TEMPERATURE_MIN = 0.1
TEMPERATURE_MAX = 1.0
TEMPERATURE_STEP = 0.1
SUPPORTED_MODELS = ["gpt-3.5-turbo", "gpt-4"]

def initialize_page() -> None:
    """Initialize the page layout and sidebar."""
    sidebar_stuff2()

def get_model_settings() -> Tuple[str, float]:
    """
    Get user-selected model settings.
    
    Returns:
        Tuple[str, float]: Selected model name and temperature setting
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
        help="Controls randomness in response generation"
    )
    
    return model_name, temperature

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
        return None
        
    try:
        return load_document(uploaded_files=uploaded_files)
    except Exception as e:
        st.error(f"Error processing PDF: {str(e)}")
        return None

def initialize_query_engine(
    documents: List,
    model_name: str,
    temperature: float
) -> None:
    """
    Initialize the query engine with the processed documents.
    
    Args:
        documents: List of processed documents
        model_name: Name of the selected GPT model
        temperature: Temperature setting for response generation
    """
    try:
        query_engine(documents, model_name, temperature)
        # Note: query_engine function handles the page switch internally
    except Exception as e:
        st.error(f"Error initializing query engine: {str(e)}")

def main() -> None:
    """Main execution flow for the PDF upload page."""
    initialize_page()
    
    # Get model settings
    model_name, temperature = get_model_settings()
    
    # Handle file upload
    documents = handle_file_upload()
    
    # Process documents if available
    if documents:
        initialize_query_engine(documents, model_name, temperature)
    else:
        st.error("Please upload a PDF file")

if __name__ == "__main__":
    main()