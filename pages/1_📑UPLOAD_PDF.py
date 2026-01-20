"""
PDF Upload and Processing Page

This module handles the PDF document upload interface and initialization of the query engine
for the Talk to PDF application. It provides model selection, temperature control, and
document processing capabilities.
"""

import os
from typing import List, Optional
import tempfile

import streamlit as st
from streamlit_extras.switch_page_button import switch_page

from functions import sidebar_stuff2, query_engine, load_document

# Constants
SUPPORTED_MODELS = ["gpt-3.5-turbo", "gpt-4"]
DEFAULT_TEMPERATURE = 0.5
TEMPERATURE_MIN = 0.1
TEMPERATURE_MAX = 1.0
TEMPERATURE_STEP = 0.1

def initialize_page() -> None:
    """Initialize the sidebar and page configuration."""
    sidebar_stuff2()

def setup_model_configuration() -> tuple[str, float]:
    """
    Set up the model selection and temperature configuration interface.
    
    Returns:
        tuple[str, float]: Selected model name and temperature value
    """
    model_name = st.selectbox(
        "Select the model you want to use",
        options=SUPPORTED_MODELS,
        help="Choose between GPT-3.5 Turbo (faster, cheaper) and GPT-4 (more capable)"
    )
    
    temperature = st.slider(
        "Set temperature",
        min_value=TEMPERATURE_MIN,
        max_value=TEMPERATURE_MAX,
        value=DEFAULT_TEMPERATURE,
        step=TEMPERATURE_STEP,
        help="Controls response creativity: lower values are more focused, higher values more diverse"
    )
    
    return model_name, temperature

def setup_file_upload() -> Optional[List]:
    """
    Configure and display the PDF file upload interface.
    
    Returns:
        Optional[List]: List of uploaded PDF files or None
    """
    return st.file_uploader(
        "Upload your PDF documents to begin the conversation 📄",
        type=['pdf'],
        accept_multiple_files=True,
        help="You can upload multiple PDF files for analysis"
    )

def process_uploaded_files(
    pdf_files: List,
    model_name: str,
    temperature: float
) -> None:
    """
    Process uploaded PDF files and initialize the query engine.
    
    Args:
        pdf_files: List of uploaded PDF files
        model_name: Selected OpenAI model name
        temperature: Temperature setting for response generation
    """
    try:
        reader = load_document(uploaded_files=pdf_files)
        engine = query_engine(reader, model_name, temperature)
        
        # Store query engine in session state for chat interface
        st.session_state['query_engine'] = engine
        st.success("✅ Documents processed successfully! You can now start chatting.")
        
    except Exception as e:
        st.error(f"Error processing documents: {str(e)}")
        st.info("Please try uploading your documents again or contact support if the issue persists.")

def main():
    """Main function to run the PDF upload page."""
    initialize_page()
    
    model_name, temperature = setup_model_configuration()
    pdf_files = setup_file_upload()
    
    if pdf_files:
        process_uploaded_files(pdf_files, model_name, temperature)
    else:
        st.info("Please upload one or more PDF files to begin")

if __name__ == "__main__":
    main()