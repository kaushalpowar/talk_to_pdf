"""
Utility functions for the Talk to PDF application.
Handles UI components, document processing, and query engine setup.
"""

import logging
import os
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

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

# UI Constants
HTML_TEMPLATE = """
<div style="background-color:{};padding:1px">
</div>
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

@dataclass
class SidebarConfig:
    """Configuration for sidebar content."""
    title: str
    content: str
    show_api_key_info: bool = False
    show_model_info: bool = False
    show_chat_info: bool = False

def create_sidebar(config: SidebarConfig) -> None:
    """
    Creates and configures the sidebar with specified content.
    
    Args:
        config: SidebarConfig object containing sidebar configuration
    """
    with st.sidebar:
        st.markdown("# ● About")
        st.markdown(
            '"Talk to PDF" is an app that allows users to ask questions about '
            'the content of a PDF file using Natural Language Processing.\n\n'
            'The app uses a question-answering system powered by OpenAI\'s GPT 🔥 '
            'to provide accurate and relevant answers to your queries.'
        )
        
        st.markdown(HTML_TEMPLATE.format("rgba(55, 53, 47, 0.16)"), unsafe_allow_html=True)
        
        if config.show_api_key_info:
            st.markdown(
                "# ● Get started\n"
                "・Paste your OpenAI API key. (click on the link to get your API key)"
            )
        
        if config.show_model_info:
            st.markdown(
                "・Choose your model (gpt-3.5-turbo or gpt-4)\n"
                "・Adjust the temperature according to your needs\n\n"
                "(It controls the randomness of the model's output. A higher temperature "
                "makes the output more diverse and random, while a lower temperature "
                "makes the output more focused and deterministic.)\n\n"
                "・Upload a PDF file and ask questions about its content"
            )
            
        if config.show_chat_info:
            st.markdown(
                "・Ask questions about your documents content\n"
                "・Get instant answers to your questions"
            )
        
        st.markdown(HTML_TEMPLATE.format("rgba(55, 53, 47, 0.16)"), unsafe_allow_html=True)
        st.markdown("Made by [Kaushal](https://twitter.com/holy_kau)")
        
        html(SUPPORT_BUTTON, height=70, width=220)
        st.markdown(BUTTON_STYLE, unsafe_allow_html=True)

# Alias functions for backwards compatibility
sidebar_stuff1 = lambda: create_sidebar(SidebarConfig(title="About", content="", show_api_key_info=True))
sidebar_stuff2 = lambda: create_sidebar(SidebarConfig(title="About", content="", show_model_info=True))
sidebar_stuff3 = lambda: create_sidebar(SidebarConfig(title="About", content="", show_chat_info=True))

def save_document(doc, documents_folder: Path) -> str:
    """
    Saves uploaded document to the specified folder.
    
    Args:
        doc: Uploaded document file
        documents_folder: Path to save documents
        
    Returns:
        str: Filename of saved document
    
    Raises:
        IOError: If file operations fail
    """
    try:
        filename = Path(doc.name).name
        documents_folder.mkdir(exist_ok=True)
        
        file_path = documents_folder / filename
        with open(file_path, 'wb') as f:
            f.write(doc.read())
            
        # Update session state
        if st.session_state.get('file_name') != filename:
            st.cache_resource.clear()
            st.session_state['file_name'] = filename
            
        return filename
    
    except Exception as e:
        logger.error(f"Error saving document: {e}")
        raise IOError(f"Failed to save document: {e}")

def remove_document(file_path: Path) -> None:
    """
    Removes document file from filesystem.
    
    Args:
        file_path: Path to document to remove
    """
    try:
        if file_path.is_file():
            file_path.unlink()
    except Exception as e:
        logger.error(f"Error removing document: {e}")

def setup_query_engine(docs: List[Document], model_name: str, temperature: float):
    """
    Sets up the query engine with the specified model and documents.
    
    Args:
        docs: List of documents to index
        model_name: Name of OpenAI model to use
        temperature: Temperature parameter for model
        
    Returns:
        Query engine instance
    """
    try:
        llm = OpenAI(model=model_name, temperature=temperature)
        Settings.llm = llm
        
        with st.spinner("Indexing document..."):
            index = VectorStoreIndex.from_documents(docs, llm=llm)
            logger.info("Document indexing completed")
            
        with st.spinner("Creating query engine..."):
            query_engine = index.as_query_engine()
            logger.info("Query engine created")
        
        # Store in session state
        st.session_state['index'] = index
        st.session_state['query_engine'] = query_engine
        
        switch_page('chat with pdf')
        return query_engine
    
    except Exception as e:
        logger.error(f"Error setting up query engine: {e}")
        st.error("Failed to setup query engine. Please try again.")
        raise

def load_documents(uploaded_files) -> List[Document]:
    """
    Loads documents from uploaded files.
    
    Args:
        uploaded_files: List of uploaded file objects
        
    Returns:
        List of loaded Document objects
    """
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir_path = Path(temp_dir)
            
            # Save uploaded files to temp directory
            for file in uploaded_files:
                temp_file_path = temp_dir_path / file.name
                temp_file_path.write_bytes(file.getvalue())
            
            # Load documents
            reader = SimpleDirectoryReader(input_dir=temp_dir)
            docs = reader.load_data()
            logger.info(f"Loaded {len(docs)} documents")
            return docs
            
    except Exception as e:
        logger.error(f"Error loading documents: {e}")
        st.error("Failed to load documents. Please try again.")
        raise