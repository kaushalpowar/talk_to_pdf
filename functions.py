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

BUTTON_STYLE = """
<style>
    iframe[width="210"] {
        position: fixed;
        bottom: 60px;
        right: 40px;
    }
</style>
"""

DIVIDER_HTML = """
<div style="background-color:{};padding:1px"></div>
"""

@dataclass
class SidebarContent:
    """Configuration for sidebar content."""
    title: str
    content: str
    divider_color: str = "rgba(55, 53, 47, 0.16)"

class PDFProcessor:
    """Handles PDF document processing and query engine setup."""
    
    def __init__(self):
        self.temp_dir = tempfile.TemporaryDirectory()
    
    def load_document(self, uploaded_files: List[st.UploadedFile]) -> List:
        """
        Load and process uploaded PDF files.
        
        Args:
            uploaded_files: List of uploaded PDF files
            
        Returns:
            List of processed documents
        """
        try:
            for file in uploaded_files:
                temp_filepath = Path(self.temp_dir.name) / file.name
                temp_filepath.write_bytes(file.getvalue())
            
            reader = SimpleDirectoryReader(input_dir=self.temp_dir.name)
            docs = reader.load_data()
            logger.info(f"Loaded {len(docs)} documents successfully")
            return docs
            
        except Exception as e:
            logger.error(f"Error loading documents: {str(e)}")
            raise

    def setup_query_engine(self, docs: List, model_name: str, temperature: float) -> Optional[VectorStoreIndex]:
        """
        Set up the query engine with the given documents and model configuration.
        
        Args:
            docs: List of processed documents
            model_name: Name of the OpenAI model to use
            temperature: Temperature parameter for the model
            
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
            
            # Navigate to chat interface
            switch_page('chat with pdf')
            return query_engine
            
        except Exception as e:
            logger.error(f"Error setting up query engine: {str(e)}")
            st.error("Failed to set up the query engine. Please try again.")
            return None

class SidebarManager:
    """Manages sidebar UI components and content."""
    
    @staticmethod
    def render_sidebar(content: SidebarContent):
        """Render sidebar with given content configuration."""
        with st.sidebar:
            st.markdown(content.title)
            st.markdown(content.content)
            st.markdown(DIVIDER_HTML.format(content.divider_color), unsafe_allow_html=True)
            
            # Author attribution and support button
            st.markdown("Made by [Kaushal](https://twitter.com/holy_kau)")
            html(SUPPORT_BUTTON_HTML, height=70, width=220)
            st.markdown(BUTTON_STYLE, unsafe_allow_html=True)

# Predefined sidebar contents
SIDEBAR_CONTENTS = {
    "api_key": SidebarContent(
        title="# ● About",
        content='''
        "Talk to PDF" is an app that allows users to ask questions about the content of a PDF file using Natural Language Processing. 
        
        The app uses a question-answering system powered by OpenAI's GPT 🔥 to provide accurate and relevant answers to your queries.
        
        # ● Get started
        ・Paste your OpenAI API key. (click on the link to get your API key)
        '''
    ),
    "upload": SidebarContent(
        title="",
        content='''
        ・Choose your model (gpt-3.5-turbo or gpt-4)
        
        ・Adjust the temperature according to your needs 
        
        (It controls the randomness of the model's output. A higher temperature (e.g., 1.0) makes the output more diverse and random, 
        while a lower temperature (e.g., 0.5) makes the output more focused and deterministic.)
       
        ・Upload a PDF file and ask questions about its content
        '''
    ),
    "chat": SidebarContent(
        title="",
        content='''
        ・Ask questions about your documents content
        
        ・Get instant answers to your questions
        '''
    )
}

# Sidebar utility functions
def sidebar_stuff1():
    """Render API key page sidebar."""
    SidebarManager.render_sidebar(SIDEBAR_CONTENTS["api_key"])

def sidebar_stuff2():
    """Render upload page sidebar."""
    SidebarManager.render_sidebar(SIDEBAR_CONTENTS["upload"])

def sidebar_stuff3():
    """Render chat page sidebar."""
    SidebarManager.render_sidebar(SIDEBAR_CONTENTS["chat"])