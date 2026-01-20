"""
Chat interface implementation for Talk to PDF application.
Handles conversation management, context-aware responses and chat UI.
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

class ChatInterface:
    """Manages the chat interface and conversation flow."""
    
    def __init__(self):
        """Initialize chat interface with query engine and index from session state."""
        self.query_engine = st.session_state['query_engine']
        self.index = st.session_state['index']
        self.chat_engine = self._initialize_chat_engine()
        
    def _initialize_chat_engine(self) -> CondenseQuestionChatEngine:
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
        
        return CondenseQuestionChatEngine.from_defaults(
            query_engine=self.query_engine,
            condense_question_prompt=custom_prompt,
            chat_history=initial_chat_history
        )

    def process_query(self, query: str) -> str:
        """
        Process user query and generate response using streaming.
        
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
            logger.error(f"Error processing query: {e}")
            return "I apologize, but I encountered an error processing your query. Please try again."

def initialize_session_state():
    """Initialize or reset session state variables."""
    if 'history' not in st.session_state:
        st.session_state['history'] = []
    if 'generated' not in st.session_state:
        st.session_state['generated'] = [DEFAULT_GREETING]
    if 'past' not in st.session_state:
        st.session_state['past'] = [DEFAULT_USER_GREETING]

def render_chat_interface(chat_interface: ChatInterface):
    """Render the chat interface and handle user interactions."""
    response_container = st.container()
    input_container = st.container()

    with input_container:
        with st.form(key='chat_form', clear_on_submit=True):
            user_input = st.text_input(
                "Query:",
                placeholder=QUERY_PLACEHOLDER,
                key='input'
            )
            submit_button = st.form_submit_button(label='Send')

        if submit_button and user_input:
            output = chat_interface.process_query(user_input)
            st.session_state['past'].append(user_input)
            st.session_state['generated'].append(output)

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
        # Initialize sidebar
        sidebar_stuff3()
        
        # Initialize session state
        initialize_session_state()
        
        # Create chat interface
        chat_interface = ChatInterface()
        
        # Initial greeting
        chat_interface.chat_engine.chat("Hello!")
        
        # Render chat interface
        render_chat_interface(chat_interface)
        
    except Exception as e:
        logger.error(f"Error in chat interface: {e}")
        st.error("An error occurred while loading the chat interface. Please refresh the page and try again.")

if __name__ == "__main__":
    main()