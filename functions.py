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

HTML_TEMP = """
<div style="background-color:{};padding:1px">
</div>
"""

@dataclass
class SidebarContent:
    """Configuration for sidebar content."""
    title: str
    content: str
    show_model_options: bool = False

def create_sidebar(content: SidebarContent) -> None:
    """
    Creates and populates the sidebar with specified content.
    
    Args:
        content: SidebarContent object containing sidebar configuration
    """
    with st.sidebar:
        if content.title:
            st.markdown(f"# ● {content.title}")
        
        st.markdown(HTML_TEMP.format("rgba(55, 53, 47, 0.16)"), unsafe_allow_html=True)
        st.markdown(content.content)
        
        if content.show_model_options:
            st.markdown("""
            ・Choose your model (gpt-3.5-turbo or gpt-4)
            ・Adjust the temperature according to your needs
            
            (Temperature controls response randomness: higher (1.0) for more diverse output, 
            lower (0.5) for more focused responses.)
            """)
        
        st.markdown(HTML_TEMP.format("rgba(55, 53, 47, 0.16)"), unsafe_allow_html=True)
        st.markdown("Made by [Kaushal](https://twitter.com/holy_kau)")
        html(BUTTON_SCRIPT, height=70, width=220)
        st.markdown(IFRAME_STYLE, unsafe_allow_html=True)

def sidebar_stuff1():
    """Creates sidebar for the API key page."""
    content = SidebarContent(
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
    create_sidebar(content)

def sidebar_stuff2():
    """Creates sidebar for the PDF upload page."""
    content = SidebarContent(
        title="",
        content="・Upload a PDF file and ask questions about its content",
        show_model_options=True
    )
    create_sidebar(content)

def sidebar_stuff3():
    """Creates sidebar for the chat interface page."""
    content = SidebarContent(
        title="",
        content="""
        ・Ask questions about your documents content
        ・Get instant answers to your questions
        """
    )
    create_sidebar(content)

class DocumentProcessor:
    """Handles document loading and processing operations."""
    
    @staticmethod
    def load_document(uploaded_files: List[st.UploadedFile]) -> List[Document]:
        """
        Loads and processes uploaded PDF files.
        
        Args:
            uploaded_files: List of uploaded PDF files
            
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

def setup_query_engine(
    docs: List[Document],
    model_name: str,
    temperature: float
) -> Optional[VectorStoreIndex]:
    """
    Sets up the query engine for document processing.
    
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
            logger.info("Query engine created successfully")
        
        # Store in session state
        st.session_state['index'] = index
        st.session_state['query_engine'] = query_engine
        
        # Navigate to chat interface
        switch_page('chat with pdf')
        return query_engine
        
    except Exception as e:
        logger.error(f"Error setting up query engine: {str(e)}")
        st.error("Failed to setup query engine. Please try again.")
        return None