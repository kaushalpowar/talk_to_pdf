"""
Chat interface implementation for Talk to PDF application.
Provides document Q&A capabilities using LlamaIndex and Streamlit.
"""

import logging
from typing import List, Optional

import streamlit as st
from streamlit_chat import message
from llama_index.core.prompts import PromptTemplate
from llama_index.core.chat_engine.condense_question import CondenseQuestionChatEngine
from llama_index.core.llms import ChatMessage, MessageRole

from functions import sidebar_stuff3

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
DEFAULT_GREETING = "Hello! Ask me anything about the uploaded document 🤗"
DEFAULT_USER_GREETING = "Hey! 👋"
QUERY_PLACEHOLDER = "What is this document about?"

# Custom prompt template for context-aware responses
CHAT_PROMPT_TEMPLATE = """\
Given a conversation (between Human and Assistant) and a follow up message from Human, \
rewrite the message to be a standalone question that captures all relevant context \
from the conversation.

<Chat History> 
{chat_history}

<Follow Up Message>
{question}

<Standalone question>
"""

class DocumentChatInterface:
    """Manages the chat interface and document Q&A functionality."""
    
    def __init__(self):
        """Initialize chat interface with query engine and session state."""
        self.setup_session_state()
        self.setup_chat_engine()
        
    def setup_session_state(self) -> None:
        """Initialize Streamlit session state variables."""
        if 'history' not in st.session_state:
            st.session_state['history'] = []
        if 'generated' not in st.session_state:
            st.session_state['generated'] = [DEFAULT_GREETING]
        if 'past' not in st.session_state:
            st.session_state['past'] = [DEFAULT_USER_GREETING]
            
    def setup_chat_engine(self) -> None:
        """Configure the chat engine with custom prompt and history."""
        try:
            self.query_engine = st.session_state['query_engine']
            self.index = st.session_state['index']
            
            custom_prompt = PromptTemplate(CHAT_PROMPT_TEMPLATE)
            custom_chat_history = [
                ChatMessage(
                    role=MessageRole.USER,
                    content='Hello assistant, given is a document. Please answer the question by understanding the context and information of the document. Use your own knowledge and understanding to answer the question.'
                ),
                ChatMessage(
                    role=MessageRole.ASSISTANT,
                    content='Okay, sounds good.'
                )
            ]
            
            self.chat_engine = CondenseQuestionChatEngine.from_defaults(
                query_engine=self.query_engine,
                condense_question_prompt=custom_prompt,
                chat_history=custom_chat_history
            )
            
            # Initialize chat
            self.chat_engine.chat("Hello!")
            
        except Exception as e:
            logger.error(f"Error setting up chat engine: {str(e)}")
            st.error("Error initializing chat interface. Please try reloading the page.")
            
    def process_query(self, query: str) -> str:
        """
        Process user query and generate response using chat engine.
        
        Args:
            query: User input query string
            
        Returns:
            Generated response string
        """
        try:
            streaming_response = self.chat_engine.stream_chat(query)
            response_tokens = []
            for token in streaming_response.response_gen:
                response_tokens.append(token)
            return ''.join(response_tokens)
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            return "Sorry, I encountered an error processing your question. Please try again."

    def render_chat_interface(self) -> None:
        """Render the chat interface components."""
        # Chat history container
        response_container = st.container()
        
        # User input container
        with st.container():
            with st.form(key='chat_form', clear_on_submit=True):
                user_input = st.text_input(
                    "Query:",
                    placeholder=QUERY_PLACEHOLDER,
                    key='input'
                )
                submit_button = st.form_submit_button(label='Send')
                
            if submit_button and user_input:
                output = self.process_query(user_input)
                st.session_state['past'].append(user_input)
                st.session_state['generated'].append(output)
        
        # Display chat history
        if st.session_state['generated']:
            with response_container:
                for i in range(len(st.session_state['generated'])):
                    message(
                        st.session_state["past"][i],
                        is_user=True,
                        key=f"{i}_user",
                        avatar_style="big-ears",
                        seed="missy"
                    )
                    message(st.session_state["generated"][i], key=str(i))

def main():
    """Main entry point for the chat interface."""
    # Setup sidebar
    sidebar_stuff3()
    
    # Initialize and render chat interface
    chat_interface = DocumentChatInterface()
    chat_interface.render_chat_interface()

if __name__ == "__main__":
    main()