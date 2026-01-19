"""
Utility functions for the Talk to PDF application.
Handles UI components, document processing, and query engine setup.
"""

import logging
import os
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import List, Optional

import streamlit as st
from streamlit.components.v1 import html
from streamlit_extras.switch_page_button import switch_page
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    Settings,
)
from llama_index.llms.openai import OpenAI

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
SUPPORT_BUTTON_HTML = """
<script type="text/javascript" src="https://cdnjs.buymeacoffee.com/1.0.0/button.prod.min.js" 
data-name="bmc-button" data-slug="kaushal.ai" data-color="#FFDD00" data-emoji=""  
data-font="Cookie" data-text="Support my work" data-outline-color="#000000" 
data-font-color="#000000" data-coffee-color="#ffffff" ></script>
"""

IFRAME_STYLE = """
<style>
    iframe[width="210"] {
        position: fixed;
        bottom: 60px;
        right: 40px;
    }
</style>
"""

class SidebarContent:
    """Manages sidebar content and styling."""
    
    @staticmethod
    def _get_divider() -> str:
        return """
        <div style="background-color:rgba(55, 53, 47, 0.16);padding:1px"></div>
        """

    @staticmethod
    def render_common_elements():
        """Renders elements common to all sidebar versions."""
        st.markdown("""Made by [Kaushal](https://twitter.com/holy_kau)""")
        html(SUPPORT_BUTTON_HTML, height=70, width=220)
        st.markdown(IFRAME_STYLE, unsafe_allow_html=True)

    @classmethod
    def render_api_key_sidebar(cls):
        """Renders sidebar for API key page."""
        with st.sidebar:
            st.markdown("""
            # ● About 
            "Talk to PDF" is an app that allows users to ask questions about the content 
            of a PDF file using Natural Language Processing. 
            
            The app uses a question-answering system powered by OpenAI's GPT 🔥 to provide 
            accurate and relevant answers to your queries.
            """)
            st.markdown(cls._get_divider(), unsafe_allow_html=True)
            st.markdown("""
            # ● Get started
            ・Paste your OpenAI API key. (click on the link to get your API key)
            """)
            st.markdown(cls._get_divider(), unsafe_allow_html=True)
            cls.render_common_elements()

    @classmethod
    def render_upload_sidebar(cls):
        """Renders sidebar for PDF upload page."""
        with st.sidebar:
            st.markdown(cls._get_divider(), unsafe_allow_html=True)
            st.markdown("""
            ・Choose your model (gpt-3.5-turbo or gpt-4)
            
            ・Adjust the temperature according to your needs 
            
            (It controls the randomness of the model's output. A higher temperature (e.g., 1.0) 
            makes the output more diverse and random, while a lower temperature (e.g., 0.5) 
            makes the output more focused and deterministic.)
            
            ・Upload a PDF file and ask questions about its content
            """)
            st.markdown(cls._get_divider(), unsafe_allow_html=True)
            cls.render_common_elements()

    @classmethod
    def render_chat_sidebar(cls):
        """Renders sidebar for chat page."""
        with st.sidebar:
            st.markdown(cls._get_divider(), unsafe_allow_html=True)
            st.markdown("""
            ・Ask questions about your documents content
            
            ・Get instant answers to your questions
            """)
            st.markdown(cls._get_divider(), unsafe_allow_html=True)
            cls.render_common_elements()

class DocumentProcessor:
    """Handles document loading and processing operations."""

    @staticmethod
    def load_document(uploaded_files: List[st.UploadedFile]) -> List:
        """
        Loads and processes uploaded PDF files.
        
        Args:
            uploaded_files: List of uploaded PDF files
            
        Returns:
            List of processed documents
        """
        with TemporaryDirectory() as temp_dir:
            temp_dir_path = Path(temp_dir)
            
            # Save uploaded files to temporary directory
            for file in uploaded_files:
                file_path = temp_dir_path / file.name
                file_path.write_bytes(file.getvalue())
            
            try:
                reader = SimpleDirectoryReader(input_dir=str(temp_dir_path))
                docs = reader.load_data()
                logger.info(f"Successfully loaded {len(docs)} documents")
                return docs
            except Exception as e:
                logger.error(f"Error loading documents: {e}")
                raise

def setup_query_engine(docs: List, model_name: str, temperature: float) -> Any:
    """
    Sets up the query engine with the given documents and model parameters.
    
    Args:
        docs: List of processed documents
        model_name: Name of the OpenAI model to use
        temperature: Temperature parameter for model output
        
    Returns:
        Configured query engine
    """
    try:
        llm = OpenAI(model=model_name, temperature=temperature)
        Settings.llm = llm
        
        with st.spinner("Indexing document..."):
            index = VectorStoreIndex.from_documents(docs, llm=llm)
            logger.info("Document indexing completed")
            
        with st.spinner("Creating query engine..."):
            query_engine = index.as_query_engine()
            logger.info("Query engine created successfully")

        # Store in session state
        st.session_state['index'] = index
        st.session_state['query_engine'] = query_engine
        
        # Navigate to chat page
        switch_page('chat with pdf')
        return query_engine
        
    except Exception as e:
        logger.error(f"Error setting up query engine: {e}")
        st.error("Failed to setup query engine. Please try again.")
        raise

# Alias functions for backwards compatibility
sidebar_stuff1 = SidebarContent.render_api_key_sidebar
sidebar_stuff2 = SidebarContent.render_upload_sidebar
sidebar_stuff3 = SidebarContent.render_chat_sidebar
load_document = DocumentProcessor.load_document
query_engine = setup_query_engine