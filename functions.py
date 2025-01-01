"""Utility functions for the Talk to PDF application."""

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional
import logging
import tempfile

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
DOCUMENTS_FOLDER = Path("documents")
BUTTON_STYLE = """
<style>
    iframe[width="210"] {
        position: fixed;
        bottom: 60px;
        right: 40px;
    }
</style>
"""

SUPPORT_BUTTON = """
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
    html_temp: str = """
        <div style="background-color:{};padding:1px">
        </div>
        """

def create_sidebar(config: SidebarConfig) -> None:
    """Create a sidebar with consistent styling and content.
    
    Args:
        config: SidebarConfig object containing sidebar settings
    """
    with st.sidebar:
        st.markdown(config.content)
        st.markdown(config.html_temp.format("rgba(55, 53, 47, 0.16)"), unsafe_allow_html=True)
        st.markdown("Made by [Kaushal](https://twitter.com/holy_kau)")
        html(SUPPORT_BUTTON, height=70, width=220)
        st.markdown(BUTTON_STYLE, unsafe_allow_html=True)

def sidebar_stuff1() -> None:
    """Display the initial sidebar with app information."""
    config = SidebarConfig(
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
    create_sidebar(config)

def sidebar_stuff2() -> None:
    """Display the model configuration sidebar."""
    config = SidebarConfig(
        title="Configuration",
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
    """Display the chat interface sidebar."""
    config = SidebarConfig(
        title="Chat",
        content="""
        ・Ask questions about your documents content
        
        ・Get instant answers to your questions
        """
    )
    create_sidebar(config)

def save_file(doc: st.uploaded_file_uploader) -> str:
    """Save uploaded file to temporary storage.
    
    Args:
        doc: Uploaded file object
    
    Returns:
        str: Filename of saved document
    
    Raises:
        IOError: If file cannot be saved
    """
    try:
        fn = Path(doc.name).name
        DOCUMENTS_FOLDER.mkdir(exist_ok=True)
        
        file_path = DOCUMENTS_FOLDER / fn
        with open(file_path, 'wb') as f:
            f.write(doc.read())
            
        if 'file_name' in st.session_state:
            if st.session_state.file_name != fn:
                st.cache_resource.clear()
                st.session_state['file_name'] = fn
        else:
            st.session_state['file_name'] = fn
            
        return fn
    
    except Exception as e:
        logger.error(f"Error saving file: {e}")
        raise IOError(f"Failed to save file: {e}")

def remove_file(file_path: str) -> None:
    """Remove processed file from temporary storage.
    
    Args:
        file_path: Path to file to be removed
    """
    try:
        path = DOCUMENTS_FOLDER / file_path
        if path.is_file():
            path.unlink()
    except Exception as e:
        logger.error(f"Error removing file: {e}")

def query_engine(docs: List[Document], model_name: str, temperature: float):
    """Create query engine for document processing.
    
    Args:
        docs: List of processed documents
        model_name: Name of OpenAI model to use
        temperature: Temperature setting for model output
        
    Returns:
        Query engine instance
    """
    try:
        llm = OpenAI(model=model_name, temperature=temperature)
        Settings.llm = llm
        
        with st.spinner("Indexing document..."):
            index = VectorStoreIndex.from_documents(docs, llm=llm)
            logger.info("Document index created")
            
        with st.spinner("Creating query engine..."):
            query_engine = index.as_query_engine()
            logger.info("Query engine created")

        st.session_state['index'] = index
        st.session_state['query_engine'] = query_engine
        switch_page('chat with pdf')
        
        return query_engine
        
    except Exception as e:
        logger.error(f"Error creating query engine: {e}")
        st.error("Failed to create query engine. Please try again.")
        raise

def load_document(uploaded_files: List[st.uploaded_file_uploader]) -> List[Document]:
    """Load and process uploaded PDF documents.
    
    Args:
        uploaded_files: List of uploaded file objects
        
    Returns:
        List of processed Document objects
    """
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir = Path(temp_dir)
            
            for file in uploaded_files:
                temp_filepath = temp_dir / file.name
                with open(temp_filepath, "wb") as f:
                    f.write(file.getvalue())

            reader = SimpleDirectoryReader(input_dir=str(temp_dir))
            docs = reader.load_data()
            logger.info(f"Loaded {len(docs)} documents")
            return docs
            
    except Exception as e:
        logger.error(f"Error loading documents: {e}")
        st.error("Failed to load documents. Please check file format and try again.")
        raise