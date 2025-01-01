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
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.text_splitter import TokenTextSplitter
from llama_index.core.indices.prompt_helper import PromptHelper

# Constants
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

class SidebarManager:
    """Manages sidebar content and styling for different pages."""
    
    @staticmethod
    def _create_base_sidebar() -> None:
        """Creates the common sidebar elements."""
        with st.sidebar:
            st.markdown(HTML_TEMPLATE.format("rgba(55, 53, 47, 0.16)"), unsafe_allow_html=True)
            st.markdown("""Made by [Kaushal](https://twitter.com/holy_kau)""")
            html(SUPPORT_BUTTON, height=70, width=220)
            st.markdown(BUTTON_STYLE, unsafe_allow_html=True)

    @staticmethod
    def create_api_sidebar() -> None:
        """Creates sidebar for API key page."""
        with st.sidebar:
            st.markdown("""
            # ● About 
            "Talk to PDF" is an app that allows users to ask questions about the content 
            of a PDF file using Natural Language Processing. 
            
            The app uses a question-answering system powered by OpenAI's GPT 🔥 to provide 
            accurate and relevant answers to your queries.
            """)
            st.markdown("""
            # ● Get started
            ・Paste your OpenAI API key. (click on the link to get your API key)
            """)
        SidebarManager._create_base_sidebar()

    @staticmethod
    def create_upload_sidebar() -> None:
        """Creates sidebar for PDF upload page."""
        with st.sidebar:
            st.markdown("""
            ・Choose your model (gpt-3.5-turbo or gpt-4)
            
            ・Adjust the temperature according to your needs 
            
            (It controls the randomness of the model's output. A higher temperature (e.g., 1.0) 
            makes the output more diverse and random, while a lower temperature (e.g., 0.5) 
            makes the output more focused and deterministic.)
            
            ・Upload a PDF file and ask questions about its content
            """)
        SidebarManager._create_base_sidebar()

    @staticmethod
    def create_chat_sidebar() -> None:
        """Creates sidebar for chat page."""
        with st.sidebar:
            st.markdown("""
            ・Ask questions about your documents content
            
            ・Get instant answers to your questions
            """)
        SidebarManager._create_base_sidebar()

class DocumentManager:
    """Handles document processing and storage operations."""

    @staticmethod
    def load_document(uploaded_files: List[Any]) -> List[Document]:
        """
        Loads and processes uploaded PDF files.
        
        Args:
            uploaded_files: List of uploaded file objects from Streamlit
            
        Returns:
            List of processed Document objects
        """
        try:
            temp_dir = tempfile.TemporaryDirectory()
            for file in uploaded_files:
                temp_filepath = os.path.join(temp_dir.name, file.name)
                with open(temp_filepath, "wb") as f:
                    f.write(file.getvalue())

            reader = SimpleDirectoryReader(input_dir=temp_dir.name)
            docs = reader.load_data()
            return docs
        except Exception as e:
            st.error(f"Error processing document: {str(e)}")
            raise

def setup_query_engine(
    docs: List[Document],
    model_name: str,
    temperature: float
) -> Any:
    """
    Sets up the query engine with the specified model and parameters.
    
    Args:
        docs: List of processed documents
        model_name: Name of the OpenAI model to use
        temperature: Temperature parameter for response generation
        
    Returns:
        Configured query engine instance
    """
    try:
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
    except Exception as e:
        st.error(f"Error setting up query engine: {str(e)}")
        raise

# Alias functions for backwards compatibility
sidebar_stuff1 = SidebarManager.create_api_sidebar
sidebar_stuff2 = SidebarManager.create_upload_sidebar
sidebar_stuff3 = SidebarManager.create_chat_sidebar
load_document = DocumentManager.load_document
query_engine = setup_query_engine