"""
Utility functions for the Talk to PDF application.
Handles UI components, document processing, and query engine setup.
"""

import logging
import os
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, TypedDict

import streamlit as st
from streamlit.components.v1 import html
from streamlit_extras.switch_page_button import switch_page
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    Settings,
    Document
)
from llama_index.llms.openai import OpenAI

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
SIDEBAR_STYLE = """
<style>
    iframe[width="210"] {
        position: fixed;
        bottom: 60px;
        right: 40px;
    }
</style>
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

@dataclass
class SidebarContent:
    """Configuration for sidebar content."""
    title: str
    description: str
    instructions: List[str]

class SessionState(TypedDict):
    """Type definitions for session state variables."""
    file_name: str
    index: VectorStoreIndex
    query_engine: any  # TODO: Add proper type for query engine

def create_sidebar(content: SidebarContent) -> None:
    """
    Creates a sidebar with specified content and styling.
    
    Args:
        content: SidebarContent object containing sidebar configuration
    """
    with st.sidebar:
        if content.title:
            st.markdown(f"# ● {content.title}")
        
        if content.description:
            st.markdown(content.description)
        
        st.markdown('<div style="background-color:rgba(55, 53, 47, 0.16);padding:1px"></div>', 
                   unsafe_allow_html=True)
        
        for instruction in content.instructions:
            st.markdown(instruction)
            
        st.markdown('<div style="background-color:rgba(55, 53, 47, 0.16);padding:1px"></div>', 
                   unsafe_allow_html=True)
        
        st.markdown('Made by [Kaushal](https://twitter.com/holy_kau)')
        html(SUPPORT_BUTTON, height=70, width=220)
        st.markdown(SIDEBAR_STYLE, unsafe_allow_html=True)

def sidebar_stuff1() -> None:
    """Creates the sidebar for the API key page."""
    content = SidebarContent(
        title="About",
        description='"Talk to PDF" is an app that allows users to ask questions about the content '
                   'of a PDF file using Natural Language Processing.\n\nThe app uses a '
                   'question-answering system powered by OpenAI\'s GPT 🔥 to provide accurate and '
                   'relevant answers to your queries.',
        instructions=["# ● Get started",
                     "・Paste your OpenAI API key. (click on the link to get your API key)"]
    )
    create_sidebar(content)

def sidebar_stuff2() -> None:
    """Creates the sidebar for the PDF upload page."""
    content = SidebarContent(
        title="",
        description="",
        instructions=[
            "・Choose your model (gpt-3.5-turbo or gpt-4)",
            "・Adjust the temperature according to your needs\n\n"
            "(It controls the randomness of the model's output. A higher temperature (e.g., 1.0) "
            "makes the output more diverse and random, while a lower temperature (e.g., 0.5) "
            "makes the output more focused and deterministic.)",
            "・Upload a PDF file and ask questions about its content"
        ]
    )
    create_sidebar(content)

def sidebar_stuff3() -> None:
    """Creates the sidebar for the chat page."""
    content = SidebarContent(
        title="",
        description="",
        instructions=[
            "・Ask questions about your documents content",
            "・Get instant answers to your questions"
        ]
    )
    create_sidebar(content)

def load_document(uploaded_files: List[st.UploadedFile]) -> List[Document]:
    """
    Loads documents from uploaded files into temporary directory.
    
    Args:
        uploaded_files: List of uploaded PDF files
        
    Returns:
        List of loaded documents
    """
    try:
        temp_dir = tempfile.TemporaryDirectory()
        for file in uploaded_files:
            temp_filepath = Path(temp_dir.name) / file.name
            temp_filepath.write_bytes(file.getvalue())

        reader = SimpleDirectoryReader(input_dir=temp_dir.name)
        docs = reader.load_data()
        logger.info(f"Successfully loaded {len(docs)} documents")
        return docs
    except Exception as e:
        logger.error(f"Error loading documents: {str(e)}")
        raise

def setup_query_engine(docs: List[Document], model_name: str, temperature: float):
    """
    Sets up the query engine with the specified model and temperature.
    
    Args:
        docs: List of loaded documents
        model_name: Name of the OpenAI model to use
        temperature: Temperature parameter for response generation
        
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
            logger.info("Query engine created")

        # Store in session state
        st.session_state['index'] = index
        st.session_state['query_engine'] = query_engine
        
        switch_page('chat with pdf')
        return query_engine
        
    except Exception as e:
        logger.error(f"Error setting up query engine: {str(e)}")
        st.error("Failed to setup query engine. Please try again.")
        raise