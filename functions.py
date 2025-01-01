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
from llama_index.embeddings.openai import OpenAIEmbedding

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# UI Constants
HTML_DIVIDER = """
    <div style="background-color:{};padding:1px">
    </div>
"""

SUPPORT_BUTTON = """
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

@dataclass
class SidebarContent:
    """Represents content configuration for different sidebar versions."""
    title: str
    description: List[str]
    instructions: List[str]

# Sidebar content configurations
SIDEBAR_CONFIGS = {
    "api_key": SidebarContent(
        title="About",
        description=[
            '"Talk to PDF" is an app that allows users to ask questions about the content of a PDF file using Natural Language Processing.',
            'The app uses a question-answering system powered by OpenAI\'s GPT 🔥 to provide accurate and relevant answers to your queries.'
        ],
        instructions=["Paste your OpenAI API key. (click on the link to get your API key)"]
    ),
    "upload": SidebarContent(
        title="Upload",
        description=[],
        instructions=[
            "Choose your model (gpt-3.5-turbo or gpt-4)",
            "Adjust the temperature according to your needs",
            "(It controls the randomness of the model's output. A higher temperature (e.g., 1.0) makes the output more diverse and random, while a lower temperature (e.g., 0.5) makes the output more focused and deterministic.)",
            "Upload a PDF file and ask questions about its content"
        ]
    ),
    "chat": SidebarContent(
        title="Chat",
        description=[],
        instructions=[
            "Ask questions about your documents content",
            "Get instant answers to your questions"
        ]
    )
}

def render_sidebar(sidebar_type: str) -> None:
    """
    Renders the sidebar with specified content configuration.
    
    Args:
        sidebar_type: Type of sidebar to render ('api_key', 'upload', or 'chat')
    """
    config = SIDEBAR_CONFIGS.get(sidebar_type)
    if not config:
        raise ValueError(f"Invalid sidebar type: {sidebar_type}")

    with st.sidebar:
        if config.title:
            st.markdown(f"# ● {config.title}")
        
        for desc in config.description:
            st.markdown(desc)
        
        st.markdown(HTML_DIVIDER.format("rgba(55, 53, 47, 0.16)"), unsafe_allow_html=True)
        
        for instruction in config.instructions:
            st.markdown(f"・{instruction}")
        
        st.markdown(HTML_DIVIDER.format("rgba(55, 53, 47, 0.16)"), unsafe_allow_html=True)
        st.markdown("Made by [Kaushal](https://twitter.com/holy_kau)")
        html(SUPPORT_BUTTON, height=70, width=220)
        st.markdown(BUTTON_STYLE, unsafe_allow_html=True)

def load_document(uploaded_files: List[st.UploadedFile]) -> List[Document]:
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

def setup_query_engine(
    docs: List[Document],
    model_name: str,
    temperature: float
) -> VectorStoreIndex:
    """
    Sets up the query engine with the specified configuration.
    
    Args:
        docs: List of processed documents
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
            logger.info("Query engine created successfully")
        
        # Store in session state for later use
        st.session_state['index'] = index
        st.session_state['query_engine'] = query_engine
        
        # Navigate to chat interface
        switch_page('chat with pdf')
        return query_engine
    
    except Exception as e:
        logger.error(f"Error setting up query engine: {str(e)}")
        st.error("Failed to setup query engine. Please try again.")
        raise

# Alias functions for backward compatibility
sidebar_stuff1 = lambda: render_sidebar('api_key')
sidebar_stuff2 = lambda: render_sidebar('upload')
sidebar_stuff3 = lambda: render_sidebar('chat')
query_engine = setup_query_engine