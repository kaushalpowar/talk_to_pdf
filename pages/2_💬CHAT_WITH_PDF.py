"""
Chat interface implementation for the Talk to PDF application.
Handles document Q&A interactions using LlamaIndex and Streamlit.
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
INITIAL_USER_MESSAGE = "Hey! 👋"
QUERY_PLACEHOLDER = "What is this document about?"

class ChatInterface:
    """Manages the chat interface and document Q&A functionality."""
    
    def __init__(self):
        """Initialize the chat interface with required components."""
        self.setup_session_state()
        self.setup_chat_engine()
        
    @staticmethod
    def setup_session_state() -> None:
        """Initialize session state variables for chat history."""
        if 'history' not in st.session_state:
            st.session_state['history'] = []
        if 'generated' not in st.session_state:
            st.session_state['generated'] = [INITIAL_GREETING]
        if 'past' not in st.session_state:
            st.session_state['past'] = [INITIAL_USER_MESSAGE]

    def setup_chat_engine(self) -> None:
        """Configure the chat engine with custom prompt and history."""
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
            
        except KeyError as e:
            logger.error(f"Failed to initialize chat engine: {str(e)}")
            st.error("Error: Please make sure you've uploaded a document first.")
            st.stop()

    def process_query(self, query: str) -> str:
        """
        Process user query and generate response using the chat engine.
        
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
        """Render the chat interface components and handle user interaction."""
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
                output = self.process_query(user_input)
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
        sidebar_stuff3()
        chat_interface = ChatInterface()
        chat_interface.render_chat_interface()
    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        st.error("An unexpected error occurred. Please refresh the page and try again.")

if __name__ == "__main__":
    main()