"""
Chat Interface Module for Talk to PDF application.
Implements an interactive chat interface using Streamlit and LlamaIndex for document Q&A.
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
        """Initialize chat interface with query engine and index from session state."""
        self.query_engine = st.session_state['query_engine']
        self.index = st.session_state['index']
        self.chat_engine = self._initialize_chat_engine()
        self._initialize_session_state()

    @staticmethod
    def _get_custom_prompt() -> PromptTemplate:
        """Returns the custom prompt template for question reformulation."""
        return PromptTemplate("""
            Given a conversation (between Human and Assistant) and a follow up message from Human, \
            rewrite the message to be a standalone question that captures all relevant context \
            from the conversation.

            <Chat History> 
            {chat_history}

            <Follow Up Message>
            {question}

            <Standalone question>
            """)

    @staticmethod
    def _get_initial_chat_history() -> List[ChatMessage]:
        """Returns the initial chat history messages."""
        return [
            ChatMessage(
                role=MessageRole.USER,
                content='Hello assistant, given is a document. Please answer the question by understanding the context and information of the document. Use your own knowledge and understanding to answer the question.'
            ),
            ChatMessage(
                role=MessageRole.ASSISTANT,
                content='Okay, sounds good.'
            )
        ]

    def _initialize_chat_engine(self) -> CondenseQuestionChatEngine:
        """Initialize and configure the chat engine."""
        try:
            chat_engine = CondenseQuestionChatEngine.from_defaults(
                query_engine=self.query_engine,
                condense_question_prompt=self._get_custom_prompt(),
                chat_history=self._get_initial_chat_history()
            )
            # Test the chat engine
            chat_engine.chat("Hello!")
            return chat_engine
        except Exception as e:
            logger.error(f"Failed to initialize chat engine: {str(e)}")
            st.error("Failed to initialize chat system. Please try refreshing the page.")
            raise

    @staticmethod
    def _initialize_session_state():
        """Initialize session state variables for chat history."""
        if 'history' not in st.session_state:
            st.session_state['history'] = []
        if 'generated' not in st.session_state:
            st.session_state['generated'] = [DEFAULT_GREETING]
        if 'past' not in st.session_state:
            st.session_state['past'] = [DEFAULT_USER_GREETING]

    def conversational_chat(self, query: str) -> str:
        """
        Process user query and generate response using streaming.
        
        Args:
            query: User input query string
            
        Returns:
            str: Generated response from the chat engine
        """
        try:
            streaming_response = self.chat_engine.stream_chat(query)
            response_tokens = []
            for token in streaming_response.response_gen:
                response_tokens.append(token)
            return ''.join(response_tokens)
        except Exception as e:
            logger.error(f"Error in chat response generation: {str(e)}")
            return "I apologize, but I encountered an error processing your request. Please try again."

    def render_chat_interface(self):
        """Render the chat interface components and handle user interaction."""
        # Create containers for chat layout
        response_container = st.container()
        input_container = st.container()

        # User input form
        with input_container:
            with st.form(key='chat_form', clear_on_submit=True):
                user_input = st.text_input(
                    "Query:",
                    placeholder=QUERY_PLACEHOLDER,
                    key='input'
                )
                submit_button = st.form_submit_button(label='Send')

            if submit_button and user_input:
                output = self.conversational_chat(user_input)
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
        sidebar_stuff3()
        chat_interface = ChatInterface()
        chat_interface.render_chat_interface()
    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        st.error("An error occurred while loading the chat interface. Please refresh the page and try again.")

if __name__ == "__main__":
    main()