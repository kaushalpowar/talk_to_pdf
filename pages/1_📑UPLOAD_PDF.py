"""
PDF Upload and Processing Page

This module handles the PDF document upload interface and initialization of the query engine
for the Talk to PDF application. It provides model selection, temperature control, and
document processing capabilities.
"""

import os
from typing import List, Optional, Tuple
import tempfile

import streamlit as st
from streamlit_extras.switch_page_button import switch_page

from functions import (
    sidebar_stuff2,
    query_engine as create_query_engine,
    save_file,
    remove_file,
    load_document
)

# Constants
SUPPORTED_MODELS = {
    "gpt-3.5-turbo": "GPT-3.5 Turbo (Faster, more economical)",
    "gpt-4": "GPT-4 (More capable, better comprehension)"
}
DEFAULT_TEMPERATURE = 0.5
TEMPERATURE_MIN = 0.1
TEMPERATURE_MAX = 1.0
TEMPERATURE_STEP = 0.1

def initialize_page() -> None:
    """Initialize the page layout and sidebar."""
    sidebar_stuff2()

def setup_model_controls() -> Tuple[str, float]:
    """
    Set up the model selection and temperature controls.
    
    Returns:
        Tuple[str, float]: Selected model name and temperature value
    """
    model_name = st.selectbox(
        "Select the model you want to use",
        options=list(SUPPORTED_MODELS.keys()),
        format_func=lambda x: SUPPORTED_MODELS[x],
        help="Choose between different GPT models based on your needs"
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

def setup_file_uploader() -> Optional[List]:
    """
    Set up the PDF file uploader interface.
    
    Returns:
        Optional[List]: List of uploaded PDF files or None
    """
    return st.file_uploader(
        "Unleash the power of AI to have a conversation with your PDFs and uncover new insights, "
        "all with a single upload ⬇️",
        type=['pdf'],
        accept_multiple_files=True,
        help="Upload one or more PDF files to analyze"
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
        model_name: Name of the selected GPT model
        temperature: Temperature setting for response generation
    """
    try:
        with st.spinner("Processing PDF files..."):
            documents = load_document(uploaded_files=pdf_files)
            
        with st.spinner("Initializing AI model..."):
            query_engine = create_query_engine(
                docs=documents,
                model_name=model_name,
                temperature=temperature
            )
            
        st.success("✅ Documents processed successfully!")
        st.info("Redirecting to chat interface...")
        
    except Exception as e:
        st.error(f"Error processing documents: {str(e)}")
        st.info("Please try uploading the files again or contact support if the issue persists.")

def main():
    """Main execution function for the PDF upload page."""
    initialize_page()
    
    model_name, temperature = setup_model_controls()
    pdf_files = setup_file_uploader()
    
    if pdf_files:
        if len(pdf_files) > 0:
            process_uploaded_files(pdf_files, model_name, temperature)
        else:
            st.warning("Please upload at least one PDF file")
    else:
        st.info("👆 Upload your PDF files above to get started")

if __name__ == "__main__":
    main()