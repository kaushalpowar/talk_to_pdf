"""
Chat Interface Module for Talk to PDF Application.

This module implements the chat interface that allows users to interact with PDF documents
using natural language queries. It uses LlamaIndex for document processing and Streamlit
for the user interface.
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

class ChatInterface:
    """Manages the chat interface and conversation logic."""
    
    def __init__(self):
        """Initialize the chat interface with required components."""
        self.setup_sidebar()
        self.initialize_chat_engine()
        self.initialize_session_state()
        self.setup_containers()

    @staticmethod
    def setup_sidebar() -> None:
        """Setup the sidebar components."""
        sidebar_stuff3()

    def initialize_chat_engine(self) -> None:
        """Initialize the chat engine with custom prompt and history."""
        try:
            self.query_engine = st.session_state['query_engine']
            self.index = st.session_state['index']
            
            custom_prompt = PromptTemplate("""
                Given a conversation (between Human and Assistant) and a follow up message from Human, \
                rewrite the message to be a standalone question that captures all relevant context \
                from the conversation.

                <Chat History> 
                {chat_history}

                <Follow Up Message>
                {question}

                <Standalone question>
            """)

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
            
            # Initialize with a greeting
            self.chat_engine.chat("Hello!")
            
        except Exception as e:
            logger.error(f"Error initializing chat engine: {str(e)}")
            st.error("Failed to initialize chat engine. Please check your configuration.")

    def initialize_session_state(self) -> None:
        """Initialize or restore session state variables."""
        if 'history' not in st.session_state:
            st.session_state['history'] = []
        if 'generated' not in st.session_state:
            st.session_state['generated'] = [DEFAULT_GREETING]
        if 'past' not in st.session_state:
            st.session_state['past'] = [DEFAULT_USER_GREETING]

    def setup_containers(self) -> None:
        """Setup Streamlit containers for chat interface."""
        self.response_container = st.container()
        self.input_container = st.container()

    def process_user_input(self, user_input: str) -> str:
        """
        Process user input and generate response using chat engine.
        
        Args:
            user_input: The user's query string
            
        Returns:
            str: Generated response from the chat engine
        """
        try:
            streaming_response = self.chat_engine.stream_chat(user_input)
            response_tokens = []
            for token in streaming_response.response_gen:
                response_tokens.append(token)
            return ''.join(response_tokens)
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            return "I apologize, but I encountered an error processing your query. Please try again."

    def render_chat_interface(self) -> None:
        """Render the chat interface with input form and message history."""
        with self.input_container:
            with st.form(key='my_form', clear_on_submit=True):
                user_input = st.text_input(
                    "Query:",
                    placeholder=QUERY_PLACEHOLDER,
                    key='input'
                )
                submit_button = st.form_submit_button(label='Send')

            if submit_button and user_input:
                output = self.process_user_input(user_input)
                st.session_state['past'].append(user_input)
                st.session_state['generated'].append(output)

        self.display_chat_history()

    def display_chat_history(self) -> None:
        """Display the chat history with user and assistant messages."""
        if st.session_state['generated']:
            with self.response_container:
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
    try:
        chat_interface = ChatInterface()
        chat_interface.render_chat_interface()
    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        st.error("An unexpected error occurred. Please refresh the page and try again.")

if __name__ == "__main__":
    main()