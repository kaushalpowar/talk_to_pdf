"""
Utility functions for the Talk to PDF application.
Handles UI components, document processing, and query engine setup.
"""

import os
from pathlib import Path
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
import tempfile

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

# UI Constants
STYLES = """
    <style>
        iframe[width="210"] {
            position: fixed;
            bottom: 60px;
            right: 40px;
        }
    </style>
"""

SUPPORT_BUTTON = """
    <script type="text/javascript" 
        src="https://cdnjs.buymeacoffee.com/1.0.0/button.prod.min.js" 
        data-name="bmc-button" 
        data-slug="kaushal.ai" 
        data-color="#FFDD00" 
        data-emoji=""  
        data-font="Cookie" 
        data-text="Support my work" 
        data-outline-color="#000000" 
        data-font-color="#000000" 
        data-coffee-color="#ffffff" >
    </script>
"""

@dataclass
class SidebarConfig:
    """Configuration for sidebar content"""
    title: str
    content: str
    show_api_warning: bool = False

def create_sidebar(config: SidebarConfig) -> None:
    """
    Creates and configures the sidebar with given content
    
    Args:
        config: SidebarConfig object containing sidebar settings
    """
    with st.sidebar:
        if config.title:
            st.markdown(f"# ● {config.title}")
        
        st.markdown(config.content)
        
        # Add divider
        st.markdown('<div style="background-color:rgba(55, 53, 47, 0.16);padding:1px"></div>', 
                   unsafe_allow_html=True)
        
        # Author info and support button
        st.markdown("Made by [Kaushal](https://twitter.com/holy_kau)")
        html(SUPPORT_BUTTON, height=70, width=220)
        st.markdown(STYLES, unsafe_allow_html=True)

def sidebar_stuff1() -> None:
    """Renders the first sidebar configuration (About page)"""
    config = SidebarConfig(
        title="About",
        content="""
        "Talk to PDF" is an app that allows users to ask questions about the content 
        of a PDF file using Natural Language Processing.
        
        The app uses a question-answering system powered by OpenAI's GPT 🔥 to provide 
        accurate and relevant answers to your queries.
        
        # ● Get started
        ・Paste your OpenAI API key. (click on the link to get your API key)
        """
    )
    create_sidebar(config)

def sidebar_stuff2() -> None:
    """Renders the second sidebar configuration (Upload page)"""
    config = SidebarConfig(
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
    create_sidebar(config)

def sidebar_stuff3() -> None:
    """Renders the third sidebar configuration (Chat page)"""
    config = SidebarConfig(
        title="",
        content="""
        ・Ask questions about your documents content
        
        ・Get instant answers to your questions
        """
    )
    create_sidebar(config)

class DocumentManager:
    """Handles document processing and storage operations"""
    
    def __init__(self, documents_folder: str = "documents"):
        self.documents_folder = Path(documents_folder)
        self.documents_folder.mkdir(exist_ok=True)

    def save_file(self, doc: Any) -> str:
        """
        Saves uploaded file and manages session state
        
        Args:
            doc: Streamlit uploaded file object
            
        Returns:
            str: Filename of saved document
        """
        filename = Path(doc.name).name
        filepath = self.documents_folder / filename
        
        with open(filepath, 'wb') as f:
            f.write(doc.read())
            
        # Update session state
        if st.session_state.get('file_name') != filename:
            st.cache_resource.clear()
            st.session_state['file_name'] = filename
            
        return filename

    def remove_file(self, filename: str) -> None:
        """
        Removes processed file from storage
        
        Args:
            filename: Name of file to remove
        """
        filepath = self.documents_folder / filename
        if filepath.exists():
            filepath.unlink()

def load_document(uploaded_files: List[Any]) -> List[Document]:
    """
    Loads documents from uploaded files into memory
    
    Args:
        uploaded_files: List of Streamlit uploaded file objects
        
    Returns:
        List[Document]: Loaded document objects
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        # Save uploaded files to temporary directory
        for file in uploaded_files:
            temp_filepath = Path(temp_dir) / file.name
            with open(temp_filepath, "wb") as f:
                f.write(file.getvalue())
        
        # Load documents using SimpleDirectoryReader
        reader = SimpleDirectoryReader(input_dir=temp_dir)
        return reader.load_data()

def setup_query_engine(
    docs: List[Document],
    model_name: str,
    temperature: float
) -> Any:
    """
    Sets up the query engine with given documents and model settings
    
    Args:
        docs: List of loaded documents
        model_name: Name of OpenAI model to use
        temperature: Temperature setting for model responses
        
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
            st.session_state['index'] = index
            
        # Setup query engine
        with st.spinner("Creating query engine..."):
            query_engine = index.as_query_engine()
            st.session_state['query_engine'] = query_engine
            
        # Switch to chat interface
        switch_page('chat with pdf')
        return query_engine
        
    except Exception as e:
        st.error(f"Error setting up query engine: {str(e)}")
        raise