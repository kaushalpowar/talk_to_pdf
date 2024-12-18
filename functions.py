"""
Utility functions for the Talk to PDF application.
Handles UI components, document processing, and query engine setup.
"""

import os
from pathlib import Path
from typing import List, Optional, Any
from dataclasses import dataclass
from tempfile import TemporaryDirectory

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

# Constants
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

@dataclass
class SidebarContent:
    """Configuration for sidebar content."""
    title: str
    content: str
    html_temp: str = """
        <div style="background-color:{};padding:1px">
        </div>
        """

class SidebarManager:
    """Manages sidebar content and styling for the application."""
    
    @staticmethod
    def _render_common_elements(content: SidebarContent) -> None:
        """Renders common sidebar elements."""
        with st.sidebar:
            st.markdown(content.html_temp.format("rgba(55, 53, 47, 0.16)"), 
                       unsafe_allow_html=True)
            st.markdown(content.content)
            st.markdown(content.html_temp.format("rgba(55, 53, 47, 0.16)"), 
                       unsafe_allow_html=True)
            st.markdown('Made by [Kaushal](https://twitter.com/holy_kau)')
            html(BUTTON_HTML, height=70, width=220)
            st.markdown(IFRAME_STYLE, unsafe_allow_html=True)

    @classmethod
    def render_api_key_sidebar(cls) -> None:
        """Renders sidebar for API key page."""
        content = SidebarContent(
            title="About",
            content="""
            # ● About 
            "Talk to PDF" is an app that allows users to ask questions about the content 
            of a PDF file using Natural Language Processing. 
            
            The app uses a question-answering system powered by OpenAI's GPT 🔥 to provide 
            accurate and relevant answers to your queries.
            
            # ● Get started
            ・Paste your OpenAI API key. (click on the link to get your API key)
            """
        )
        cls._render_common_elements(content)

    @classmethod
    def render_upload_sidebar(cls) -> None:
        """Renders sidebar for PDF upload page."""
        content = SidebarContent(
            title="Upload",
            content="""
            ・Choose your model (gpt-3.5-turbo or gpt-4)
            
            ・Adjust the temperature according to your needs 
            
            (It controls the randomness of the model's output. A higher temperature (e.g., 1.0) 
            makes the output more diverse and random, while a lower temperature (e.g., 0.5) 
            makes the output more focused and deterministic.)
           
            ・Upload a PDF file and ask questions about its content
            """
        )
        cls._render_common_elements(content)

    @classmethod
    def render_chat_sidebar(cls) -> None:
        """Renders sidebar for chat interface."""
        content = SidebarContent(
            title="Chat",
            content="""
            ・Ask questions about your documents content
            
            ・Get instant answers to your questions
            """
        )
        cls._render_common_elements(content)

class DocumentProcessor:
    """Handles document processing and query engine setup."""
    
    @staticmethod
    def load_document(uploaded_files: List[Any]) -> List[Document]:
        """
        Loads and processes uploaded PDF files.
        
        Args:
            uploaded_files: List of uploaded file objects from Streamlit
            
        Returns:
            List of processed Document objects
        """
        with TemporaryDirectory() as temp_dir:
            for file in uploaded_files:
                temp_filepath = Path(temp_dir) / file.name
                with open(temp_filepath, "wb") as f:
                    f.write(file.getvalue())

            reader = SimpleDirectoryReader(input_dir=temp_dir)
            docs = reader.load_data()
            return docs

    @staticmethod
    def setup_query_engine(docs: List[Document], 
                          model_name: str, 
                          temperature: float) -> Any:
        """
        Sets up the query engine for document processing.
        
        Args:
            docs: List of processed documents
            model_name: Name of the OpenAI model to use
            temperature: Temperature setting for response generation
            
        Returns:
            Configured query engine instance
        """
        llm = OpenAI(model=model_name, temperature=temperature)
        Settings.llm = llm
        
        with st.spinner("Indexing document..."):
            index = VectorStoreIndex.from_documents(docs, llm=llm)
            
        with st.spinner("Creating query engine..."):
            query_engine = index.as_query_engine()

        # Store in session state for later use
        st.session_state['index'] = index
        st.session_state['query_engine'] = query_engine
        
        switch_page('chat with pdf')
        return query_engine

# Alias functions for backwards compatibility
sidebar_stuff1 = SidebarManager.render_api_key_sidebar
sidebar_stuff2 = SidebarManager.render_upload_sidebar
sidebar_stuff3 = SidebarManager.render_chat_sidebar
load_document = DocumentProcessor.load_document
query_engine = DocumentProcessor.setup_query_engine