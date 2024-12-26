"""
Utility functions for the Talk to PDF application.
Handles UI components, document processing, and query engine setup.
"""

import logging
from pathlib import Path
from dataclasses import dataclass
from typing import List, Optional
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

# UI Constants
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
class SidebarConfig:
    """Configuration for sidebar content."""
    title: str
    content: str
    button: str = BUTTON_HTML
    style: str = IFRAME_STYLE

def create_sidebar(config: SidebarConfig) -> None:
    """
    Creates a sidebar with consistent styling and content.
    
    Args:
        config: SidebarConfig containing sidebar content and styling
    """
    with st.sidebar:
        if config.title:
            st.markdown(f"# {config.title}")
        
        st.markdown(config.content)
        st.markdown("""<div style="background-color:rgba(55, 53, 47, 0.16);padding:1px"></div>""", 
                   unsafe_allow_html=True)
        
        st.markdown("""Made by [Kaushal](https://twitter.com/holy_kau)""")
        html(config.button, height=70, width=220)
        st.markdown(config.style, unsafe_allow_html=True)

def sidebar_stuff1():
    """Creates the sidebar for the API key page."""
    config = SidebarConfig(
        title="● About",
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

def sidebar_stuff2():
    """Creates the sidebar for the PDF upload page."""
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

def sidebar_stuff3():
    """Creates the sidebar for the chat page."""
    config = SidebarConfig(
        title="",
        content="""
        ・Ask questions about your documents content
        
        ・Get instant answers to your questions
        """
    )
    create_sidebar(config)

class DocumentProcessor:
    """Handles document loading and processing operations."""
    
    def __init__(self, documents_folder: str = "documents"):
        self.documents_folder = Path(documents_folder)
        self.documents_folder.mkdir(exist_ok=True)

    def save_file(self, doc) -> str:
        """
        Saves uploaded file and manages session state.
        
        Args:
            doc: Uploaded file object
            
        Returns:
            str: Filename of saved document
        """
        filename = Path(doc.name).name
        file_path = self.documents_folder / filename
        
        with open(file_path, 'wb') as f:
            f.write(doc.read())
            
        if st.session_state.get('file_name') != filename:
            st.cache_resource.clear()
            st.session_state['file_name'] = filename
            
        return filename

    def remove_file(self, filename: str) -> None:
        """
        Removes processed file from storage.
        
        Args:
            filename: Name of file to remove
        """
        file_path = self.documents_folder / filename
        if file_path.exists():
            file_path.unlink()

    @staticmethod
    def load_document(uploaded_files: List) -> List[Document]:
        """
        Loads documents from uploaded files into memory.
        
        Args:
            uploaded_files: List of uploaded file objects
            
        Returns:
            List[Document]: Loaded document objects
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir_path = Path(temp_dir)
            
            for file in uploaded_files:
                temp_file_path = temp_dir_path / file.name
                with open(temp_file_path, "wb") as f:
                    f.write(file.getvalue())

            reader = SimpleDirectoryReader(input_dir=temp_dir)
            docs = reader.load_data()
            logger.info(f"Loaded {len(docs)} documents")
            return docs

def setup_query_engine(docs: List[Document], 
                      model_name: str, 
                      temperature: float) -> VectorStoreIndex:
    """
    Sets up the query engine with the specified configuration.
    
    Args:
        docs: List of documents to index
        model_name: Name of the OpenAI model to use
        temperature: Temperature parameter for response generation
        
    Returns:
        VectorStoreIndex: Configured query engine
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
        
        # Navigate to chat page
        switch_page('chat with pdf')
        return query_engine
        
    except Exception as e:
        logger.error(f"Error setting up query engine: {str(e)}")
        st.error("Failed to setup query engine. Please try again.")
        raise