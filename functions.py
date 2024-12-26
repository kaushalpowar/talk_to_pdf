"""
Utility functions for the Talk to PDF application.
Handles document processing, UI components, and OpenAI integration.
"""

import os
from pathlib import Path
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
import tempfile
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

# UI Constants
BUTTON_HTML = """
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

DIV_TEMPLATE = """
<div style="background-color:{};padding:1px">
</div>
"""

@dataclass
class SidebarContent:
    """Configuration for sidebar content."""
    title: str
    content: str
    additional_content: Optional[str] = None

def create_sidebar(content: SidebarContent) -> None:
    """
    Creates a sidebar with consistent styling and content.
    
    Args:
        content: SidebarContent object containing sidebar configuration
    """
    with st.sidebar:
        if content.title:
            st.markdown(f"# ● {content.title}")
        
        st.markdown(content.content)
        st.markdown(DIV_TEMPLATE.format("rgba(55, 53, 47, 0.16)"), unsafe_allow_html=True)
        
        if content.additional_content:
            st.markdown(content.additional_content)
            st.markdown(DIV_TEMPLATE.format("rgba(55, 53, 47, 0.16)"), unsafe_allow_html=True)
        
        st.markdown('Made by [Kaushal](https://twitter.com/holy_kau)')
        html(BUTTON_HTML, height=70, width=220)
        st.markdown(IFRAME_STYLE, unsafe_allow_html=True)

def sidebar_stuff1() -> None:
    """Creates the sidebar for the API key page."""
    content = SidebarContent(
        title="About",
        content="""
        "Talk to PDF" is an app that allows users to ask questions about the content 
        of a PDF file using Natural Language Processing.
        
        The app uses a question-answering system powered by OpenAI's GPT 🔥 to provide 
        accurate and relevant answers to your queries.
        """,
        additional_content="""
        # ● Get started
        ・Paste your OpenAI API key. (click on the link to get your API key)
        """
    )
    create_sidebar(content)

def sidebar_stuff2() -> None:
    """Creates the sidebar for the PDF upload page."""
    content = SidebarContent(
        title="",
        content="""
        ・Choose your model (gpt-3.5-turbo or gpt-4)
        
        ・Adjust the temperature according to your needs 
        
        (It controls the randomness of the model's output. A higher temperature (e.g., 1.0) 
        makes the output more diverse and random, while a lower temperature (e.g., 0.5) 
        makes the output more focused and deterministic.)
       
        ・Upload a PDF file and ask questions about its content
        """
    )
    create_sidebar(content)

def sidebar_stuff3() -> None:
    """Creates the sidebar for the chat interface page."""
    content = SidebarContent(
        title="",
        content="""
        ・Ask questions about your documents content
        
        ・Get instant answers to your questions
        """
    )
    create_sidebar(content)

def load_document(uploaded_files: List[Any]) -> List[Document]:
    """
    Loads and processes uploaded PDF files.
    
    Args:
        uploaded_files: List of uploaded file objects from Streamlit
        
    Returns:
        List of processed Document objects
        
    Raises:
        Exception: If document loading fails
    """
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            # Save uploaded files to temporary directory
            for file in uploaded_files:
                temp_filepath = Path(temp_dir) / file.name
                temp_filepath.write_bytes(file.getvalue())
            
            # Load documents using SimpleDirectoryReader
            reader = SimpleDirectoryReader(input_dir=temp_dir)
            docs = reader.load_data()
            logger.info(f"Successfully loaded {len(docs)} documents")
            return docs
            
    except Exception as e:
        logger.error(f"Error loading documents: {str(e)}")
        raise

def query_engine(
    docs: List[Document],
    model_name: str,
    temperature: float
) -> Any:
    """
    Creates a query engine for document interaction.
    
    Args:
        docs: List of processed documents
        model_name: Name of the OpenAI model to use
        temperature: Temperature setting for response generation
        
    Returns:
        Configured query engine object
        
    Raises:
        Exception: If engine creation fails
    """
    try:
        # Initialize OpenAI model
        llm = OpenAI(model=model_name, temperature=temperature)
        Settings.llm = llm
        
        # Create document index
        with st.spinner("Indexing document..."):
            index = VectorStoreIndex.from_documents(docs, llm=llm)
            logger.info("Document index created successfully")
        
        # Create query engine
        with st.spinner("Creating query engine..."):
            query_engine = index.as_query_engine()
            logger.info("Query engine created successfully")
        
        # Store in session state
        st.session_state['index'] = index
        st.session_state['query_engine'] = query_engine
        
        # Navigate to chat interface
        switch_page('chat with pdf')
        return query_engine
        
    except Exception as e:
        logger.error(f"Error creating query engine: {str(e)}")
        st.error("Failed to create query engine. Please try again.")
        raise