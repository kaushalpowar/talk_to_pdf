"""
Utility functions for the Talk to PDF application.
Handles UI components, document processing, and query engine setup.
"""

import os
import tempfile
from typing import List, Optional, Dict, Any
import logging
from pathlib import Path

import streamlit as st
from streamlit.components.v1 import html
from streamlit_extras.switch_page_button import switch_page
import openai
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    Settings,
    Document
)
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.text_splitter import TokenTextSplitter

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
TEMPERATURE_RANGE = (0.1, 1.0)
DEFAULT_TEMPERATURE = 0.5
SUPPORTED_MODELS = ["gpt-3.5-turbo", "gpt-4"]

# HTML/CSS Templates
SIDEBAR_DIVIDER = """
<div style="background-color:{};padding:1px"></div>
"""

SUPPORT_BUTTON = """
<script type="text/javascript" src="https://cdnjs.buymeacoffee.com/1.0.0/button.prod.min.js" 
    data-name="bmc-button" 
    data-slug="kaushal.ai" 
    data-color="#FFDD00" 
    data-emoji=""  
    data-font="Cookie" 
    data-text="Support my work" 
    data-outline-color="#000000" 
    data-font-color="#000000" 
    data-coffee-color="#ffffff">
</script>
"""

BUTTON_STYLE = """
<style>
    iframe[width="210"] {
        position: fixed;
        bottom: 60px;
        right: 40px;
    }
</style>
"""

class SidebarManager:
    """Manages sidebar content and styling for different application pages."""
    
    @staticmethod
    def _add_common_elements() -> None:
        """Adds common sidebar elements like author credit and support button."""
        st.markdown("""Made by [Kaushal](https://twitter.com/holy_kau)""")
        html(SUPPORT_BUTTON, height=70, width=220)
        st.markdown(BUTTON_STYLE, unsafe_allow_html=True)

    @staticmethod
    def api_key_page() -> None:
        """Renders sidebar for API key input page."""
        with st.sidebar:
            st.markdown("""
            # ● About 
            "Talk to PDF" is an app that allows users to ask questions about the content 
            of a PDF file using Natural Language Processing. 
            
            The app uses a question-answering system powered by OpenAI's GPT 🔥 to provide 
            accurate and relevant answers to your queries.
            """)
            st.markdown(SIDEBAR_DIVIDER.format("rgba(55, 53, 47, 0.16)"), unsafe_allow_html=True)
            st.markdown("""
            # ● Get started
            ・Paste your OpenAI API key. (click on the link to get your API key)
            """)
            st.markdown(SIDEBAR_DIVIDER.format("rgba(55, 53, 47, 0.16)"), unsafe_allow_html=True)
            SidebarManager._add_common_elements()

    @staticmethod
    def upload_page() -> None:
        """Renders sidebar for PDF upload page."""
        with st.sidebar:
            st.markdown(SIDEBAR_DIVIDER.format("rgba(55, 53, 47, 0.16)"), unsafe_allow_html=True)
            st.markdown("""
            ・Choose your model (gpt-3.5-turbo or gpt-4)
            
            ・Adjust the temperature according to your needs 
            
            (Temperature controls the randomness of the model's output. Higher values (e.g., 1.0) 
            produce more diverse and creative responses, while lower values (e.g., 0.5) produce 
            more focused and deterministic responses.)
            
            ・Upload a PDF file and ask questions about its content
            """)
            st.markdown(SIDEBAR_DIVIDER.format("rgba(55, 53, 47, 0.16)"), unsafe_allow_html=True)
            SidebarManager._add_common_elements()

    @staticmethod
    def chat_page() -> None:
        """Renders sidebar for chat interface page."""
        with st.sidebar:
            st.markdown(SIDEBAR_DIVIDER.format("rgba(55, 53, 47, 0.16)"), unsafe_allow_html=True)
            st.markdown("""
            ・Ask questions about your documents content
            
            ・Get instant answers to your questions
            """)
            st.markdown(SIDEBAR_DIVIDER.format("rgba(55, 53, 47, 0.16)"), unsafe_allow_html=True)
            SidebarManager._add_common_elements()

class DocumentManager:
    """Handles document processing and storage operations."""

    def __init__(self, documents_folder: str = "documents"):
        self.documents_folder = Path(documents_folder)
        self.documents_folder.mkdir(exist_ok=True)

    def save_file(self, doc: Any) -> str:
        """
        Saves uploaded file to temporary storage and manages file state.
        
        Args:
            doc: Streamlit uploaded file object
            
        Returns:
            str: Filename of saved document
        """
        filename = Path(doc.name).name
        file_path = self.documents_folder / filename
        
        with open(file_path, 'wb') as f:
            f.write(doc.read())
            
        # Update session state
        if 'file_name' in st.session_state:
            if st.session_state.file_name != filename:
                st.cache_resource.clear()
                st.session_state['file_name'] = filename
        else:
            st.session_state['file_name'] = filename
            
        return filename

    def remove_file(self, filename: str) -> None:
        """Removes processed file from temporary storage."""
        file_path = self.documents_folder / filename
        if file_path.exists():
            file_path.unlink()

    @staticmethod
    def load_document(uploaded_files: List[Any]) -> List[Document]:
        """
        Processes uploaded PDF files and converts them to document objects.
        
        Args:
            uploaded_files: List of Streamlit uploaded file objects
            
        Returns:
            List[Document]: Processed document objects
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            # Save uploaded files to temporary directory
            for file in uploaded_files:
                temp_path = Path(temp_dir) / file.name
                with open(temp_path, "wb") as f:
                    f.write(file.getvalue())

            # Process documents
            reader = SimpleDirectoryReader(input_dir=temp_dir)
            docs = reader.load_data()
            logger.info(f"Processed {len(docs)} documents")
            return docs

def setup_query_engine(
    docs: List[Document],
    model_name: str,
    temperature: float
) -> Any:
    """
    Sets up the query engine for document processing.
    
    Args:
        docs: List of processed documents
        model_name: Name of the OpenAI model to use
        temperature: Temperature parameter for response generation
        
    Returns:
        Query engine instance
    """
    try:
        # Initialize language model
        llm = OpenAI(model=model_name, temperature=temperature)
        Settings.llm = llm

        # Create document index
        with st.spinner("Indexing document..."):
            index = VectorStoreIndex.from_documents(docs, llm=llm)
            logger.info("Document index created successfully")

        # Setup query engine
        with st.spinner("Creating query engine..."):
            query_engine = index.as_query_engine()
            logger.info("Query engine initialized")

        # Store in session state
        st.session_state['index'] = index
        st.session_state['query_engine'] = query_engine

        # Navigate to chat interface
        switch_page('chat with pdf')
        return query_engine

    except Exception as e:
        logger.error(f"Error setting up query engine: {str(e)}")
        st.error("Failed to initialize query engine. Please try again.")
        raise

# Initialize sidebar functions for backwards compatibility
sidebar_stuff1 = SidebarManager.api_key_page
sidebar_stuff2 = SidebarManager.upload_page
sidebar_stuff3 = SidebarManager.chat_page