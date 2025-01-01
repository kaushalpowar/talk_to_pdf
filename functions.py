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
DOCUMENTS_FOLDER = Path("documents")
BUTTON_STYLE = """
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
class SidebarConfig:
    """Configuration for sidebar content."""
    title: str
    content: str
    divider_color: str = "rgba(55, 53, 47, 0.16)"

def create_sidebar(config: SidebarConfig) -> None:
    """
    Creates a sidebar with consistent styling and content.
    
    Args:
        config: SidebarConfig object containing sidebar settings
    """
    with st.sidebar:
        if config.title:
            st.markdown(f"# ● {config.title}")
        
        st.markdown(config.content)
        st.markdown(f'<div style="background-color:{config.divider_color};padding:1px"></div>', 
                   unsafe_allow_html=True)
        
        st.markdown('Made by [Kaushal](https://twitter.com/holy_kau)')
        html(BUTTON_STYLE, height=70, width=220)
        st.markdown(IFRAME_STYLE, unsafe_allow_html=True)

def sidebar_stuff1() -> None:
    """Renders the API key input sidebar."""
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
    """Renders the model configuration sidebar."""
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
    """Renders the chat interface sidebar."""
    config = SidebarConfig(
        title="",
        content="""
        ・Ask questions about your documents content
        
        ・Get instant answers to your questions
        """
    )
    create_sidebar(config)

def save_file(doc: Any) -> str:
    """
    Saves uploaded file to documents folder and manages session state.
    
    Args:
        doc: Streamlit uploaded file object
    
    Returns:
        str: Name of saved file
    """
    if not DOCUMENTS_FOLDER.exists():
        DOCUMENTS_FOLDER.mkdir(parents=True)
        
    filename = Path(doc.name).name
    filepath = DOCUMENTS_FOLDER / filename
    
    with open(filepath, 'wb') as f:
        f.write(doc.read())
    
    if 'file_name' in st.session_state:
        if st.session_state.file_name != filename:
            st.cache_resource.clear()
            st.session_state['file_name'] = filename
    else:
        st.session_state['file_name'] = filename
        
    return filename

def remove_file(filename: str) -> None:
    """
    Removes file from documents folder.
    
    Args:
        filename: Name of file to remove
    """
    filepath = DOCUMENTS_FOLDER / filename
    if filepath.exists():
        filepath.unlink()

def setup_query_engine(docs: List[Document], model_name: str, temperature: float):
    """
    Sets up the query engine with the given documents and model configuration.
    
    Args:
        docs: List of processed documents
        model_name: Name of OpenAI model to use
        temperature: Temperature setting for model responses
        
    Returns:
        QueryEngine: Configured query engine
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
        return None

def load_document(uploaded_files: List[Any]) -> Optional[List[Document]]:
    """
    Loads and processes uploaded PDF files.
    
    Args:
        uploaded_files: List of Streamlit uploaded file objects
        
    Returns:
        Optional[List[Document]]: Processed documents if successful, None otherwise
    """
    try:
        with TemporaryDirectory() as temp_dir:
            for file in uploaded_files:
                temp_filepath = Path(temp_dir) / file.name
                with open(temp_filepath, "wb") as f:
                    f.write(file.getvalue())

            reader = SimpleDirectoryReader(input_dir=temp_dir)
            return reader.load_data()
            
    except Exception as e:
        st.error(f"Error loading document: {str(e)}")
        return None