"""
PDF Upload and Processing Page

This module handles the PDF document upload interface and model configuration for the
Talk to PDF application. It provides a user interface for selecting AI models,
configuring parameters, and processing PDF documents for analysis.
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
SUPPORTED_MODELS = ["gpt-3.5-turbo", "gpt-4"]
DEFAULT_MODEL = "gpt-3.5-turbo"
MIN_TEMPERATURE = 0.1
MAX_TEMPERATURE = 1.0
DEFAULT_TEMPERATURE = 0.5
TEMPERATURE_STEP = 0.1

def initialize_page() -> None:
    """Initialize the page sidebar and layout."""
    sidebar_stuff2()

def configure_model() -> Tuple[str, float]:
    """
    Configure the AI model settings.
    
    Returns:
        Tuple[str, float]: Selected model name and temperature setting
    """
    model_name = st.selectbox(
        "Select the model you want to use",
        options=SUPPORTED_MODELS,
        index=SUPPORTED_MODELS.index(DEFAULT_MODEL)
    )
    
    temperature = st.slider(
        "Set temperature",
        min_value=MIN_TEMPERATURE,
        max_value=MAX_TEMPERATURE,
        value=DEFAULT_TEMPERATURE,
        step=TEMPERATURE_STEP,
        help="Controls response creativity. Higher values produce more diverse outputs."
    )
    
    return model_name, temperature

def handle_file_upload() -> Optional[List]:
    """
    Handle PDF file upload process.
    
    Returns:
        Optional[List]: Processed document data if successful, None otherwise
    """
    uploaded_files = st.file_uploader(
        "Unleash the power of AI to have a conversation with your PDFs "
        "and uncover new insights, all with a single upload ⬇️",
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

def process_documents(documents: List, model_name: str, temperature: float) -> None:
    """
    Process uploaded documents and initialize query engine.
    
    Args:
        documents: List of processed documents
        model_name: Name of the selected AI model
        temperature: Temperature setting for the model
    """
    try:
        with st.spinner("Processing documents..."):
            engine = query_engine(documents, model_name, temperature)
            st.success("Documents processed successfully!")
            st.info("Redirecting to chat interface...")
    except Exception as e:
        st.error(f"Error creating query engine: {str(e)}")
        st.info("Please try again or contact support if the issue persists.")

def main():
    """Main execution function for the PDF upload page."""
    initialize_page()
    
    # Configure AI model settings
    model_name, temperature = configure_model()
    
    # Handle document upload
    documents = handle_file_upload()
    
    # Process documents if uploaded
    if documents:
        process_documents(documents, model_name, temperature)
    else:
        st.info("Please upload a PDF file to begin")

if __name__ == "__main__":
    main()