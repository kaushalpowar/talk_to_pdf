"""
Chat interface implementation for the Talk to PDF application.
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
AVATAR_STYLE = "big-ears"
AVATAR_SEED = "missy"

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
    """Manages the chat interface and conversation logic."""
    
    def __init__(self):
        """Initialize chat interface with query engine and index from session state."""
        self.query_engine = st.session_state.get('query_engine')
        self.index = st.session_state.get('index')
        
        if not self.query_engine or not self.index:
            st.error("Query engine or index not found in session state. Please upload a document first.")
            st.stop()
            
        self.initialize_chat_engine()
        self.initialize_session_state()
        
    def initialize_chat_engine(self):
        """Set up the chat engine with custom prompt and initial context."""
        custom_prompt = PromptTemplate(CHAT_PROMPT_TEMPLATE)
        
        initial_chat_history = [
            ChatMessage(
                role=MessageRole.USER,
                content='Hello assistant, given is a document. Please answer the question by understanding the context and information of the document. Use your own knowledge and understanding to answer the question.'
            ),
            ChatMessage(
                role=MessageRole.ASSISTANT,
                content='Okay, sounds good.'
            )
        ]
        
        try:
            self.chat_engine = CondenseQuestionChatEngine.from_defaults(
                query_engine=self.query_engine,
                condense_question_prompt=custom_prompt,
                chat_history=initial_chat_history
            )
        except Exception as e:
            logger.error(f"Failed to initialize chat engine: {str(e)}")
            st.error("Failed to initialize chat system. Please try refreshing the page.")
            st.stop()
    
    def initialize_session_state(self):
        """Initialize or get session state variables."""
        if 'history' not in st.session_state:
            st.session_state['history'] = []
        if 'generated' not in st.session_state:
            st.session_state['generated'] = [DEFAULT_GREETING]
        if 'past' not in st.session_state:
            st.session_state['past'] = [DEFAULT_USER_GREETING]
    
    def process_user_input(self, user_input: str) -> str:
        """
        Process user input and generate response using chat engine.
        
        Args:
            user_input: The user's question or message
            
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
            logger.error(f"Error processing user input: {str(e)}")
            return "I apologize, but I encountered an error processing your question. Please try again."
    
    def render_chat_interface(self):
        """Render the chat interface with message history."""
        # Create containers for chat components
        response_container = st.container()
        input_container = st.container()
        
        # User input form
        with input_container:
            with st.form(key='chat_form', clear_on_submit=True):
                user_input = st.text_input(
                    "Query:",
                    placeholder="What is this document about?",
                    key='input'
                )
                submit_button = st.form_submit_button(label='Send')
                
            if submit_button and user_input:
                output = self.process_user_input(user_input)
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
                        avatar_style=AVATAR_STYLE,
                        seed=AVATAR_SEED
                    )
                    message(st.session_state["generated"][i], key=str(i))

def main():
    """Main entry point for the chat interface."""
    # Setup sidebar
    sidebar_stuff3()
    
    try:
        # Initialize and render chat interface
        chat_interface = ChatInterface()
        chat_interface.render_chat_interface()
    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        st.error("An unexpected error occurred. Please refresh the page and try again.")

if __name__ == "__main__":
    main()