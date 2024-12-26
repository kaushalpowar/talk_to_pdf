"""
Utility functions for the Talk to PDF application.
Handles UI components, document processing, and OpenAI integration.
"""

import os
import tempfile
from dataclasses import dataclass
from pathlib import Path
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
DOCUMENTS_FOLDER = "documents"
DEFAULT_TEMPERATURE = 0.5
SUPPORT_BUTTON_HTML = """
<script type="text/javascript" src="https://cdnjs.buymeacoffee.com/1.0.0/button.prod.min.js" 
data-name="bmc-button" data-slug="kaushal.ai" data-color="#FFDD00" data-emoji=""  
data-font="Cookie" data-text="Support my work" data-outline-color="#000000" 
data-font-color="#000000" data-coffee-color="#ffffff" ></script>
"""

@dataclass
class SidebarConfig:
    """Configuration for sidebar content."""
    title: str
    content: str
    show_api_warning: bool = False

def create_sidebar_html(bg_color: str = "rgba(55, 53, 47, 0.16)") -> str:
    """Creates HTML template for sidebar divider."""
    return f"""
    <div style="background-color:{bg_color};padding:1px">
    </div>
    """

def add_support_button() -> None:
    """Adds the 'Buy Me a Coffee' support button to the sidebar."""
    html(SUPPORT_BUTTON_HTML, height=70, width=220)
    st.markdown(
        """
        <style>
            iframe[width="210"] {
                position: fixed;
                bottom: 60px;
                right: 40px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

def render_sidebar(config: SidebarConfig) -> None:
    """Renders sidebar with specified configuration."""
    with st.sidebar:
        st.markdown(f"# ● {config.title}")
        st.markdown(config.content)
        
        if config.show_api_warning:
            st.warning("⚠️ Please enter OpenAI API key")
            
        st.markdown(create_sidebar_html())
        st.markdown("Made by [Kaushal](https://twitter.com/holy_kau)")
        add_support_button()

def sidebar_stuff1() -> None:
    """Renders the first sidebar configuration."""
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
    render_sidebar(config)

def sidebar_stuff2() -> None:
    """Renders the second sidebar configuration."""
    config = SidebarConfig(
        title="Options",
        content="""
        ・Choose your model (gpt-3.5-turbo or gpt-4)
        
        ・Adjust the temperature according to your needs
        
        (It controls the randomness of the model's output. A higher temperature (e.g., 1.0) 
        makes the output more diverse and random, while a lower temperature (e.g., 0.5) 
        makes the output more focused and deterministic.)
        
        ・Upload a PDF file and ask questions about its content
        """
    )
    render_sidebar(config)

def sidebar_stuff3() -> None:
    """Renders the third sidebar configuration."""
    config = SidebarConfig(
        title="Instructions",
        content="""
        ・Ask questions about your documents content
        
        ・Get instant answers to your questions
        """
    )
    render_sidebar(config)

def save_file(doc: Any) -> str:
    """
    Saves uploaded file to documents folder and manages session state.
    
    Args:
        doc: Streamlit uploaded file object
    
    Returns:
        str: Filename of saved document
    """
    try:
        filename = Path(doc.name).name
        documents_path = Path(DOCUMENTS_FOLDER)
        
        # Create documents directory if it doesn't exist
        documents_path.mkdir(exist_ok=True)
        
        # Save file
        file_path = documents_path / filename
        file_path.write_bytes(doc.read())
        
        # Update session state
        if st.session_state.get('file_name') != filename:
            st.cache_resource.clear()
            st.session_state['file_name'] = filename
            
        return filename
    
    except Exception as e:
        st.error(f"Error saving file: {str(e)}")
        raise

def remove_file(file_path: str) -> None:
    """
    Removes file from documents folder after processing.
    
    Args:
        file_path: Path to file to be removed
    """
    try:
        full_path = Path(DOCUMENTS_FOLDER) / file_path
        if full_path.is_file():
            full_path.unlink()
    except Exception as e:
        st.warning(f"Error removing temporary file: {str(e)}")

def load_document(uploaded_files: List[Any]) -> List[Document]:
    """
    Loads documents from uploaded files into memory.
    
    Args:
        uploaded_files: List of Streamlit uploaded file objects
    
    Returns:
        List[Document]: Loaded documents
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        # Save uploaded files to temporary directory
        for file in uploaded_files:
            temp_path = Path(temp_dir) / file.name
            temp_path.write_bytes(file.getvalue())
        
        # Load documents using LlamaIndex
        reader = SimpleDirectoryReader(input_dir=temp_dir)
        return reader.load_data()

def query_engine(
    docs: List[Document],
    model_name: str,
    temperature: float = DEFAULT_TEMPERATURE
) -> Any:
    """
    Creates and configures the query engine for document processing.
    
    Args:
        docs: List of documents to process
        model_name: Name of the OpenAI model to use
        temperature: Temperature setting for model output
    
    Returns:
        Query engine instance
    """
    try:
        # Configure LLM
        llm = OpenAI(model=model_name, temperature=temperature)
        Settings.llm = llm
        
        # Create document index
        with st.spinner("Indexing document..."):
            index = VectorStoreIndex.from_documents(docs, llm=llm)
            st.session_state['index'] = index
        
        # Create query engine
        with st.spinner("Creating query engine..."):
            query_engine = index.as_query_engine()
            st.session_state['query_engine'] = query_engine
        
        # Switch to chat interface
        switch_page('chat with pdf')
        return query_engine
    
    except Exception as e:
        st.error(f"Error creating query engine: {str(e)}")
        raise