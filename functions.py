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
from llama_index.core import (Settings, SimpleDirectoryReader, VectorStoreIndex,
                             set_global_service_context)
from llama_index.core.indices.prompt_helper import PromptHelper
from llama_index.core.text_splitter import TokenTextSplitter
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from streamlit.components.v1 import html
from streamlit_extras.switch_page_button import switch_page

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
BUTTON_HTML = """
<script type="text/javascript" src="https://cdnjs.buymeacoffee.com/1.0.0/button.prod.min.js" 
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
<div style="background-color:{};padding:1px"></div>
"""

@dataclass
class SidebarConfig:
    """Configuration for sidebar content."""
    about_text: str
    instructions: List[str]
    background_color: str = "rgba(55, 53, 47, 0.16)"
    author_link: str = "[Kaushal](https://twitter.com/holy_kau)"

def create_sidebar(config: SidebarConfig) -> None:
    """
    Creates a sidebar with specified configuration.
    
    Args:
        config: SidebarConfig object containing sidebar settings
    """
    with st.sidebar:
        if config.about_text:
            st.markdown(f"# ● About\n{config.about_text}")
        
        st.markdown(DIV_TEMPLATE.format(config.background_color), unsafe_allow_html=True)
        
        for instruction in config.instructions:
            st.markdown(instruction)
            
        st.markdown(DIV_TEMPLATE.format(config.background_color), unsafe_allow_html=True)
        st.markdown(f"Made by {config.author_link}")
        html(BUTTON_HTML, height=70, width=220)
        st.markdown(IFRAME_STYLE, unsafe_allow_html=True)

def sidebar_stuff1():
    """Creates sidebar for API key page."""
    config = SidebarConfig(
        about_text='"Talk to PDF" is an app that allows users to ask questions about the content '
                  'of a PDF file using Natural Language Processing.\n\nThe app uses a question-answering '
                  'system powered by OpenAI\'s GPT 🔥 to provide accurate and relevant answers to your queries.',
        instructions=["# ● Get started", "・Paste your OpenAI API key. (click on the link to get your API key)"]
    )
    create_sidebar(config)

def sidebar_stuff2():
    """Creates sidebar for PDF upload page."""
    config = SidebarConfig(
        about_text="",
        instructions=[
            "・Choose your model (gpt-3.5-turbo or gpt-4)",
            "・Adjust the temperature according to your needs\n\n"
            "(It controls the randomness of the model's output. A higher temperature (e.g., 1.0) "
            "makes the output more diverse and random, while a lower temperature (e.g., 0.5) "
            "makes the output more focused and deterministic.)",
            "・Upload a PDF file and ask questions about its content"
        ]
    )
    create_sidebar(config)

def sidebar_stuff3():
    """Creates sidebar for chat page."""
    config = SidebarConfig(
        about_text="",
        instructions=[
            "・Ask questions about your documents content",
            "・Get instant answers to your questions"
        ]
    )
    create_sidebar(config)

def load_document(uploaded_files: List[st.UploadedFile]) -> List:
    """
    Loads and processes uploaded PDF files.
    
    Args:
        uploaded_files: List of uploaded PDF files
        
    Returns:
        List of processed documents
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

def query_engine(docs: List, model_name: str, temperature: float):
    """
    Creates and configures the query engine for document processing.
    
    Args:
        docs: List of processed documents
        model_name: Name of the OpenAI model to use
        temperature: Temperature setting for response generation
        
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
        
        switch_page('chat with pdf')
        return query_engine
        
    except Exception as e:
        logger.error(f"Error creating query engine: {str(e)}")
        st.error("Failed to create query engine. Please try again.")
        raise