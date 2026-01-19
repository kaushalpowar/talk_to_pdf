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
from llama_index.core import (
    Settings,
    SimpleDirectoryReader,
    VectorStoreIndex,
)
from llama_index.llms.openai import OpenAI
from streamlit.components.v1 import html
from streamlit_extras.switch_page_button import switch_page

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
    Creates a sidebar with specified configuration.
    
    Args:
        config: SidebarConfig object containing sidebar settings
    """
    with st.sidebar:
        if config.title:
            st.markdown(f"# ● {config.title}")
        
        st.markdown(config.content)
        
        # Add divider
        st.markdown(
            '<div style="background-color:rgba(55, 53, 47, 0.16);padding:1px"></div>',
            unsafe_allow_html=True
        )
        
        # Author info and support button
        st.markdown('Made by [Kaushal](https://twitter.com/holy_kau)')
        html(SUPPORT_BUTTON_HTML, height=70, width=220)
        st.markdown(IFRAME_STYLE, unsafe_allow_html=True)

def sidebar_stuff1() -> None:
    """Creates sidebar for API key page."""
    config = SidebarConfig(
        title="About",
        content="""
        "Talk to PDF" is an app that allows users to ask questions about the content 
        of a PDF file using Natural Language Processing.
        
        The app uses a question-answering system powered by OpenAI's GPT 🔥 to provide 
        accurate and relevant answers to your queries.
        
        # ● Get started
        ・Paste your OpenAI API key. (click on the link to get your API key)
        """,
        show_api_key_info=True
    )
    create_sidebar(config)

def sidebar_stuff2() -> None:
    """Creates sidebar for PDF upload page."""
    config = SidebarConfig(
        title="",
        content="""
        ・Choose your model (gpt-3.5-turbo or gpt-4)
        
        ・Adjust the temperature according to your needs
        
        (It controls the randomness of the model's output. A higher temperature (e.g., 1.0) 
        makes the output more diverse and random, while a lower temperature (e.g., 0.5) 
        makes the output more focused and deterministic.)
        
        ・Upload a PDF file and ask questions about its content
        """,
        show_model_info=True
    )
    create_sidebar(config)

def sidebar_stuff3() -> None:
    """Creates sidebar for chat page."""
    config = SidebarConfig(
        title="",
        content="""
        ・Ask questions about your documents content
        
        ・Get instant answers to your questions
        """,
        show_chat_info=True
    )
    create_sidebar(config)

def save_file(doc) -> str:
    """
    Saves uploaded file and manages session state.
    
    Args:
        doc: Uploaded file object
    
    Returns:
        str: Filename of saved document
    """
    try:
        documents_folder = Path("documents")
        documents_folder.mkdir(exist_ok=True)
        
        filename = Path(doc.name).name
        file_path = documents_folder / filename
        
        with open(file_path, 'wb') as f:
            f.write(doc.read())
            
        # Update session state
        if st.session_state.get('file_name') != filename:
            st.cache_resource.clear()
            st.session_state['file_name'] = filename
            
        return filename
    
    except Exception as e:
        logger.error(f"Error saving file: {e}")
        st.error("Failed to save uploaded file")
        raise

def remove_file(file_path: str) -> None:
    """
    Removes processed file from documents folder.
    
    Args:
        file_path: Path to file to be removed
    """
    try:
        path = Path("documents") / file_path
        if path.exists():
            path.unlink()
    except Exception as e:
        logger.error(f"Error removing file: {e}")

def load_document(uploaded_files: List) -> List:
    """
    Loads documents from uploaded files.
    
    Args:
        uploaded_files: List of uploaded file objects
    
    Returns:
        List: Loaded document objects
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        for file in uploaded_files:
            temp_path = Path(temp_dir) / file.name
            with open(temp_path, "wb") as f:
                f.write(file.getvalue())
        
        reader = SimpleDirectoryReader(input_dir=temp_dir)
        docs = reader.load_data()
        logger.info(f"Loaded {len(docs)} documents")
        return docs

def query_engine(docs: List, model_name: str, temperature: float) -> Optional:
    """
    Creates and configures query engine for document processing.
    
    Args:
        docs: List of document objects
        model_name: Name of OpenAI model to use
        temperature: Temperature setting for model
    
    Returns:
        Optional: Configured query engine
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
        
        # Navigate to chat page
        switch_page('chat with pdf')
        return query_engine
        
    except Exception as e:
        logger.error(f"Error creating query engine: {e}")
        st.error("Failed to process document")
        raise