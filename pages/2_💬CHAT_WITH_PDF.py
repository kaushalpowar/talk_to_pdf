"""
Chat interface implementation for the Talk to PDF application.
Handles conversation management and document Q&A using LlamaIndex and Streamlit.
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
INITIAL_GREETING = "Hello! Ask me anything about the uploaded document 🤗"
INITIAL_USER_MSG = "Hey! 👋"
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

class ChatInterface:
    """Manages the chat interface and conversation flow."""
    
    def __init__(self):
        """Initialize chat interface with required components."""
        self._initialize_session_state()
        self._setup_chat_engine()
        
    def _initialize_session_state(self) -> None:
        """Initialize Streamlit session state variables."""
        if 'history' not in st.session_state:
            st.session_state['history'] = []
        if 'generated' not in st.session_state:
            st.session_state['generated'] = [INITIAL_GREETING]
        if 'past' not in st.session_state:
            st.session_state['past'] = [INITIAL_USER_MSG]

    def _setup_chat_engine(self) -> None:
        """Configure the chat engine with custom prompt and history."""
        try:
            # Get query engine from session state
            self.query_engine = st.session_state['query_engine']
            self.index = st.session_state['index']
            
            # Initialize custom prompt
            custom_prompt = PromptTemplate(CHAT_PROMPT_TEMPLATE)
            
            # Set up initial chat history
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
            
            # Create chat engine
            self.chat_engine = CondenseQuestionChatEngine.from_defaults(
                query_engine=self.query_engine,
                condense_question_prompt=custom_prompt,
                chat_history=custom_chat_history
            )
            
            # Initial greeting
            self.chat_engine.chat("Hello!")
            
        except Exception as e:
            logger.error(f"Error setting up chat engine: {str(e)}")
            st.error("Failed to initialize chat engine. Please try reloading the page.")

    def _process_chat(self, query: str) -> str:
        """
        Process user query and generate response.
        
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
            logger.error(f"Error processing chat: {str(e)}")
            return "I apologize, but I encountered an error processing your request. Please try again."

    def render(self) -> None:
        """Render the chat interface."""
        # Add sidebar
        sidebar_stuff3()
        
        # Create containers for chat
        response_container = st.container()
        input_container = st.container()
        
        # Handle user input
        with input_container:
            with st.form(key='chat_form', clear_on_submit=True):
                user_input = st.text_input(
                    "Query:",
                    placeholder=QUERY_PLACEHOLDER,
                    key='input'
                )
                submit_button = st.form_submit_button(label='Send')
                
            if submit_button and user_input:
                output = self._process_chat(user_input)
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
    try:
        chat_interface = ChatInterface()
        chat_interface.render()
    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        st.error("An unexpected error occurred. Please refresh the page and try again.")

if __name__ == "__main__":
    main()