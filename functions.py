"""
Utility functions for the Talk to PDF application.
Handles UI components, document processing, and query engine setup.
"""

import os
import tempfile
from pathlib import Path
from typing import List, Optional, Dict, Any
import logging

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
from llama_index.core.indices.prompt_helper import PromptHelper

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
BUTTON_STYLE = """
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

class SidebarManager:
    """Manages sidebar content and styling for different pages."""
    
    @staticmethod
    def _get_html_template(color: str = "rgba(55, 53, 47, 0.16)") -> str:
        """Returns HTML template with specified background color."""
        return f'<div style="background-color:{color};padding:1px"></div>'

    @staticmethod
    def _add_common_elements() -> None:
        """Adds common elements to all sidebars."""
        st.markdown("Made by [Kaushal](https://twitter.com/holy_kau)")
        html(BUTTON_STYLE, height=70, width=220)
        st.markdown(IFRAME_STYLE, unsafe_allow_html=True)

    def render_api_key_sidebar(self) -> None:
        """Renders sidebar for API key page."""
        with st.sidebar:
            st.markdown("""
            # ● About 
            "Talk to PDF" is an app that allows users to ask questions about the content 
            of a PDF file using Natural Language Processing. 
            
            The app uses a question-answering system powered by OpenAI's GPT 🔥 to provide 
            accurate and relevant answers to your queries.
            """)
            st.markdown(self._get_html_template(), unsafe_allow_html=True)
            st.markdown("""
            # ● Get started
            ・Paste your OpenAI API key. (click on the link to get your API key)
            """)
            st.markdown(self._get_html_template(), unsafe_allow_html=True)
            self._add_common_elements()

    def render_upload_sidebar(self) -> None:
        """Renders sidebar for PDF upload page."""
        with st.sidebar:
            st.markdown(self._get_html_template(), unsafe_allow_html=True)
            st.markdown("""
            ・Choose your model (gpt-3.5-turbo or gpt-4)
            
            ・Adjust the temperature according to your needs 
            
            (It controls the randomness of the model's output. A higher temperature (e.g., 1.0) 
            makes the output more diverse and random, while a lower temperature (e.g., 0.5) 
            makes the output more focused and deterministic.)
            
            ・Upload a PDF file and ask questions about its content
            """)
            st.markdown(self._get_html_template(), unsafe_allow_html=True)
            self._add_common_elements()

    def render_chat_sidebar(self) -> None:
        """Renders sidebar for chat page."""
        with st.sidebar:
            st.markdown(self._get_html_template(), unsafe_allow_html=True)
            st.markdown("""
            ・Ask questions about your documents content
            
            ・Get instant answers to your questions
            """)
            st.markdown(self._get_html_template(), unsafe_allow_html=True)
            self._add_common_elements()

class DocumentProcessor:
    """Handles document loading and processing operations."""

    @staticmethod
    def load_document(uploaded_files: List[Any]) -> List[Document]:
        """
        Loads and processes uploaded PDF files.
        
        Args:
            uploaded_files: List of uploaded file objects from Streamlit
            
        Returns:
            List of processed Document objects
        """
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                for file in uploaded_files:
                    temp_filepath = Path(temp_dir) / file.name
                    temp_filepath.write_bytes(file.getvalue())

                reader = SimpleDirectoryReader(input_dir=temp_dir)
                docs = reader.load_data()
                logger.info(f"Successfully loaded {len(docs)} documents")
                return docs
        except Exception as e:
            logger.error(f"Error loading documents: {str(e)}")
            raise

class QueryEngineManager:
    """Manages query engine setup and configuration."""

    @staticmethod
    def setup_query_engine(
        docs: List[Document],
        model_name: str,
        temperature: float
    ) -> Any:
        """
        Sets up and configures the query engine.
        
        Args:
            docs: List of processed documents
            model_name: Name of the OpenAI model to use
            temperature: Temperature setting for the model
            
        Returns:
            Configured query engine instance
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
            logger.error(f"Error setting up query engine: {str(e)}")
            st.error("Failed to setup query engine. Please try again.")
            raise

# Initialize managers
sidebar_manager = SidebarManager()
document_processor = DocumentProcessor()
query_engine_manager = QueryEngineManager()

# Alias functions for backwards compatibility
sidebar_stuff1 = sidebar_manager.render_api_key_sidebar
sidebar_stuff2 = sidebar_manager.render_upload_sidebar
sidebar_stuff3 = sidebar_manager.render_chat_sidebar
load_document = document_processor.load_document
query_engine = query_engine_manager.setup_query_engine