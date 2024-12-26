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
BUTTON_SCRIPT = """
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
    about_text: str
    instructions: str
    divider_color: str = "rgba(55, 53, 47, 0.16)"

def create_sidebar_content(config: SidebarConfig) -> None:
    """
    Creates and displays sidebar content based on provided configuration.
    
    Args:
        config: SidebarConfig object containing sidebar content and styling
    """
    with st.sidebar:
        if config.about_text:
            st.markdown(config.about_text)
        
        st.markdown(f'<div style="background-color:{config.divider_color};padding:1px"></div>', 
                   unsafe_allow_html=True)
        
        if config.instructions:
            st.markdown(config.instructions)
            
        st.markdown(f'<div style="background-color:{config.divider_color};padding:1px"></div>', 
                   unsafe_allow_html=True)
        
        st.markdown('Made by [Kaushal](https://twitter.com/holy_kau)')
        html(BUTTON_SCRIPT, height=70, width=220)
        st.markdown(IFRAME_STYLE, unsafe_allow_html=True)

def sidebar_stuff1():
    """Displays the initial sidebar with API key instructions."""
    config = SidebarConfig(
        about_text="""
        # ● About 
        "Talk to PDF" is an app that allows users to ask questions about the content 
        of a PDF file using Natural Language Processing. 
        
        The app uses a question-answering system powered by OpenAI's GPT 🔥 to provide 
        accurate and relevant answers to your queries.
        """,
        instructions="""
        # ● Get started
        ・Paste your OpenAI API key. (click on the link to get your API key)
        """
    )
    create_sidebar_content(config)

def sidebar_stuff2():
    """Displays the PDF upload sidebar with model selection instructions."""
    config = SidebarConfig(
        about_text="",
        instructions="""
        ・Choose your model (gpt-3.5-turbo or gpt-4)
        
        ・Adjust the temperature according to your needs 
        
        (It controls the randomness of the model's output. A higher temperature (e.g., 1.0) 
        makes the output more diverse and random, while a lower temperature (e.g., 0.5) 
        makes the output more focused and deterministic.)
       
        ・Upload a PDF file and ask questions about its content
        """
    )
    create_sidebar_content(config)

def sidebar_stuff3():
    """Displays the chat interface sidebar."""
    config = SidebarConfig(
        about_text="",
        instructions="""
        ・Ask questions about your documents content
        
        ・Get instant answers to your questions
        """
    )
    create_sidebar_content(config)

def save_file(doc) -> str:
    """
    Saves uploaded file to temporary storage and manages session state.
    
    Args:
        doc: Streamlit uploaded file object
    
    Returns:
        str: Filename of saved document
    
    Raises:
        OSError: If file operations fail
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
    
    except OSError as e:
        logger.error(f"Failed to save file: {e}")
        raise

def remove_file(file_path: str) -> None:
    """
    Removes processed file from temporary storage.
    
    Args:
        file_path: Path to file to be removed
    """
    try:
        path = Path("documents") / file_path
        if path.exists():
            path.unlink()
    except OSError as e:
        logger.error(f"Failed to remove file: {e}")

def setup_query_engine(docs: List[Document], model_name: str, temperature: float):
    """
    Sets up the query engine with specified model configuration.
    
    Args:
        docs: List of processed documents
        model_name: Name of the OpenAI model to use
        temperature: Temperature setting for response generation
    
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
            logger.info("Query engine created")
        
        # Store in session state
        st.session_state['index'] = index
        st.session_state['query_engine'] = query_engine
        
        # Navigate to chat interface
        switch_page('chat with pdf')
        return query_engine
    
    except Exception as e:
        logger.error(f"Failed to setup query engine: {e}")
        st.error("Failed to setup document processing. Please try again.")
        raise

def load_document(uploaded_files) -> List[Document]:
    """
    Processes uploaded PDF files into document objects.
    
    Args:
        uploaded_files: List of Streamlit uploaded file objects
    
    Returns:
        List[Document]: Processed document objects
    """
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            for file in uploaded_files:
                temp_filepath = Path(temp_dir) / file.name
                with open(temp_filepath, "wb") as f:
                    f.write(file.getvalue())
            
            reader = SimpleDirectoryReader(input_dir=temp_dir)
            docs = reader.load_data()
            logger.info(f"Loaded {len(docs)} documents successfully")
            return docs
            
    except Exception as e:
        logger.error(f"Failed to load documents: {e}")
        st.error("Failed to process uploaded files. Please try again.")
        raise