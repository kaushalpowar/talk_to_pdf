"""
Utility functions for the Talk to PDF application.
Handles UI components, document processing, and query engine setup.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional
import logging
import tempfile
import os

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

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
DOCUMENTS_FOLDER = "documents"
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

HTML_DIVIDER = """
<div style="background-color:{};padding:1px">
</div>
"""

@dataclass
class SidebarContent:
    """Configuration for sidebar content."""
    title: str
    description: str
    instructions: List[str]

def create_sidebar_common(content: Optional[SidebarContent] = None) -> None:
    """
    Creates a common sidebar with customizable content.
    
    Args:
        content: Optional SidebarContent object with custom sidebar information
    """
    with st.sidebar:
        if content:
            if content.title:
                st.markdown(f"# ● {content.title}")
            if content.description:
                st.markdown(content.description)
            
        st.markdown(HTML_DIVIDER.format("rgba(55, 53, 47, 0.16)"), unsafe_allow_html=True)
        
        if content and content.instructions:
            for instruction in content.instructions:
                st.markdown(instruction)
            st.markdown(HTML_DIVIDER.format("rgba(55, 53, 47, 0.16)"), unsafe_allow_html=True)

        st.markdown('Made by [Kaushal](https://twitter.com/holy_kau)')
        html(BUTTON_SCRIPT, height=70, width=220)
        st.markdown(IFRAME_STYLE, unsafe_allow_html=True)

def sidebar_stuff1() -> None:
    """Creates the sidebar for the API key page."""
    content = SidebarContent(
        title="About",
        description='"Talk to PDF" is an app that allows users to ask questions about '
                   'the content of a PDF file using Natural Language Processing.\n\n'
                   'The app uses a question-answering system powered by OpenAI\'s GPT 🔥 '
                   'to provide accurate and relevant answers to your queries.',
        instructions=["# ● Get started",
                     "・Paste your OpenAI API key. (click on the link to get your API key)"]
    )
    create_sidebar_common(content)

def sidebar_stuff2() -> None:
    """Creates the sidebar for the PDF upload page."""
    content = SidebarContent(
        title="",
        description="",
        instructions=[
            "・Choose your model (gpt-3.5-turbo or gpt-4)",
            "・Adjust the temperature according to your needs\n\n"
            "(It controls the randomness of the model's output. A higher temperature "
            "(e.g., 1.0) makes the output more diverse and random, while a lower "
            "temperature (e.g., 0.5) makes the output more focused and deterministic.)",
            "・Upload a PDF file and ask questions about its content"
        ]
    )
    create_sidebar_common(content)

def sidebar_stuff3() -> None:
    """Creates the sidebar for the chat interface page."""
    content = SidebarContent(
        title="",
        description="",
        instructions=[
            "・Ask questions about your documents content",
            "・Get instant answers to your questions"
        ]
    )
    create_sidebar_common(content)

def save_file(doc: st.uploaded_file_buffer) -> str:
    """
    Saves an uploaded file to the documents folder.
    
    Args:
        doc: Streamlit uploaded file buffer
    
    Returns:
        str: Name of the saved file
    
    Raises:
        OSError: If file operations fail
    """
    try:
        documents_path = Path(DOCUMENTS_FOLDER)
        documents_path.mkdir(exist_ok=True)
        
        filename = Path(doc.name).name
        file_path = documents_path / filename
        
        with open(file_path, 'wb') as f:
            f.write(doc.read())
            
        # Update session state
        if 'file_name' in st.session_state and st.session_state.file_name != filename:
            st.cache_resource.clear()
        st.session_state['file_name'] = filename
        
        return filename
    
    except Exception as e:
        logger.error(f"Error saving file: {str(e)}")
        raise OSError(f"Failed to save file: {str(e)}")

def remove_file(file_path: str) -> None:
    """
    Removes a file from the documents folder.
    
    Args:
        file_path: Path to the file to remove
    """
    try:
        full_path = Path(DOCUMENTS_FOLDER) / file_path
        if full_path.is_file():
            full_path.unlink()
    except Exception as e:
        logger.error(f"Error removing file: {str(e)}")

def load_document(uploaded_files: List[st.uploaded_file_buffer]) -> List[Document]:
    """
    Loads documents from uploaded files into memory.
    
    Args:
        uploaded_files: List of Streamlit uploaded file buffers
    
    Returns:
        List[Document]: List of loaded documents
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

def query_engine(docs: List[Document], model_name: str, temperature: float):
    """
    Creates a query engine for the loaded documents.
    
    Args:
        docs: List of loaded documents
        model_name: Name of the OpenAI model to use
        temperature: Temperature parameter for response generation
    
    Returns:
        QueryEngine: Configured query engine
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
        
        switch_page('chat with pdf')
        return query_engine
    
    except Exception as e:
        logger.error(f"Error creating query engine: {str(e)}")
        st.error("Failed to create query engine. Please try again.")
        raise