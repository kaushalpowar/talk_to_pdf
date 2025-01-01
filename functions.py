"""
Utility functions for the Talk to PDF application.
Handles UI components, document processing, and query engine setup.
"""

import os
import tempfile
from typing import List, Optional, Dict, Any

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
from llama_index.core.query_engine import QueryEngine

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

class SidebarManager:
    """Manages sidebar content and styling for different pages."""
    
    @staticmethod
    def _create_common_elements(content: str) -> None:
        """Creates common sidebar elements across pages."""
        with st.sidebar:
            st.markdown(
                """<div style="background-color:rgba(55, 53, 47, 0.16);padding:1px"></div>""",
                unsafe_allow_html=True
            )
            st.markdown(content)
            st.markdown(
                """Made by [Kaushal](https://twitter.com/holy_kau)"""
            )
            html(SUPPORT_BUTTON_HTML, height=70, width=220)
            st.markdown(IFRAME_STYLE, unsafe_allow_html=True)

    @classmethod
    def render_api_key_page(cls) -> None:
        """Renders sidebar for API key page."""
        content = """
        # ● About 
        "Talk to PDF" is an app that allows users to ask questions about the content 
        of a PDF file using Natural Language Processing. 
        
        The app uses a question-answering system powered by OpenAI's GPT 🔥 to provide 
        accurate and relevant answers to your queries.
        
        # ● Get started
        ・Paste your OpenAI API key. (click on the link to get your API key)
        """
        cls._create_common_elements(content)

    @classmethod
    def render_upload_page(cls) -> None:
        """Renders sidebar for PDF upload page."""
        content = """
        ・Choose your model (gpt-3.5-turbo or gpt-4)
        
        ・Adjust the temperature according to your needs 
        
        (It controls the randomness of the model's output. A higher temperature (e.g., 1.0) 
        makes the output more diverse and random, while a lower temperature (e.g., 0.5) 
        makes the output more focused and deterministic.)
       
        ・Upload a PDF file and ask questions about its content
        """
        cls._create_common_elements(content)

    @classmethod
    def render_chat_page(cls) -> None:
        """Renders sidebar for chat page."""
        content = """
        ・Ask questions about your documents content
        
        ・Get instant answers to your questions
        """
        cls._create_common_elements(content)

class DocumentManager:
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
        with tempfile.TemporaryDirectory() as temp_dir:
            for file in uploaded_files:
                temp_filepath = os.path.join(temp_dir, file.name)
                with open(temp_filepath, "wb") as f:
                    f.write(file.getvalue())
            
            reader = SimpleDirectoryReader(input_dir=temp_dir)
            docs = reader.load_data()
            return docs

class QueryEngineManager:
    """Manages query engine setup and configuration."""

    @staticmethod
    def setup_query_engine(
        docs: List[Document],
        model_name: str,
        temperature: float
    ) -> QueryEngine:
        """
        Sets up the query engine with the given parameters.
        
        Args:
            docs: List of processed documents
            model_name: Name of the OpenAI model to use
            temperature: Temperature parameter for response generation
            
        Returns:
            Configured query engine instance
        """
        llm = OpenAI(model=model_name, temperature=temperature)
        Settings.llm = llm
        
        with st.spinner("Indexing document..."):
            index = VectorStoreIndex.from_documents(docs, llm=llm)
            st.session_state['index'] = index
        
        with st.spinner("Creating query engine..."):
            query_engine = index.as_query_engine()
            st.session_state['query_engine'] = query_engine
        
        switch_page('chat with pdf')
        return query_engine

def initialize_session_state() -> None:
    """Initializes or resets session state variables."""
    if 'index' not in st.session_state:
        st.session_state['index'] = None
    if 'query_engine' not in st.session_state:
        st.session_state['query_engine'] = None
    if 'file_name' not in st.session_state:
        st.session_state['file_name'] = None

# Alias functions for backwards compatibility
sidebar_stuff1 = SidebarManager.render_api_key_page
sidebar_stuff2 = SidebarManager.render_upload_page
sidebar_stuff3 = SidebarManager.render_chat_page
load_document = DocumentManager.load_document
query_engine = QueryEngineManager.setup_query_engine