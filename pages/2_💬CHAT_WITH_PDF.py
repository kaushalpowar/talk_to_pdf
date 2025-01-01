"""
Chat interface implementation for the Talk to PDF application.
Handles conversation management, response generation and UI rendering.
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

class ChatConfig:
    """Configuration for the chat interface"""
    
    CUSTOM_PROMPT_TEMPLATE = """\
        Given a conversation (between Human and Assistant) and a follow up message from Human, \
        rewrite the message to be a standalone question that captures all relevant context \
        from the conversation.

        <Chat History> 
        {chat_history}

        <Follow Up Message>
        {question}

        <Standalone question>
        """

    INITIAL_CHAT_HISTORY = [
        ChatMessage(
            role=MessageRole.USER,
            content='Hello assistant, given is a document. Please answer the question by understanding the context and information of the document. Use your own knowledge and understanding to answer the question.'
        ),
        ChatMessage(
            role=MessageRole.ASSISTANT,
            content='Okay, sounds good.'
        )
    ]

class ChatEngine:
    """Handles chat functionality and state management"""

    def __init__(self, query_engine):
        """Initialize chat engine with query engine"""
        self.query_engine = query_engine
        self.custom_prompt = PromptTemplate(ChatConfig.CUSTOM_PROMPT_TEMPLATE)
        self.chat_engine = self._initialize_chat_engine()

    def _initialize_chat_engine(self) -> CondenseQuestionChatEngine:
        """Initialize the condense question chat engine"""
        try:
            return CondenseQuestionChatEngine.from_defaults(
                query_engine=self.query_engine,
                condense_question_prompt=self.custom_prompt,
                chat_history=ChatConfig.INITIAL_CHAT_HISTORY
            )
        except Exception as e:
            logger.error(f"Failed to initialize chat engine: {e}")
            raise

    def get_response(self, query: str) -> str:
        """Generate response for user query with streaming"""
        try:
            streaming_response = self.chat_engine.stream_chat(query)
            return ''.join(streaming_response.response_gen)
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return "I apologize, but I encountered an error processing your request."

class ChatInterface:
    """Handles UI components and state management"""

    def __init__(self):
        """Initialize chat interface and state"""
        self._initialize_session_state()
        sidebar_stuff3()
        
        # Initialize chat engine
        self.query_engine = st.session_state.get('query_engine')
        if not self.query_engine:
            st.error("Query engine not initialized. Please upload a document first.")
            return
            
        self.chat_engine = ChatEngine(self.query_engine)

    @staticmethod
    def _initialize_session_state():
        """Initialize session state variables"""
        if 'history' not in st.session_state:
            st.session_state['history'] = []
        if 'generated' not in st.session_state:
            st.session_state['generated'] = [DEFAULT_GREETING]
        if 'past' not in st.session_state:
            st.session_state['past'] = [DEFAULT_USER_GREETING]

    def render_chat_history(self):
        """Render chat history messages"""
        with st.container() as response_container:
            for i in range(len(st.session_state['generated'])):
                message(
                    st.session_state["past"][i],
                    is_user=True,
                    key=f"{i}_user",
                    avatar_style="big-ears",
                    seed="missy"
                )
                message(st.session_state["generated"][i], key=str(i))

    def render_input_form(self):
        """Render input form and handle user input"""
        with st.container() as container:
            with st.form(key='chat_form', clear_on_submit=True):
                user_input = st.text_input(
                    "Query:",
                    placeholder=QUERY_PLACEHOLDER,
                    key='input'
                )
                submit_button = st.form_submit_button(label='Send')

            if submit_button and user_input:
                self._handle_user_input(user_input)

    def _handle_user_input(self, user_input: str):
        """Process user input and generate response"""
        try:
            output = self.chat_engine.get_response(user_input)
            st.session_state['past'].append(user_input)
            st.session_state['generated'].append(output)
        except Exception as e:
            logger.error(f"Error handling user input: {e}")
            st.error("An error occurred while processing your request.")

def main():
    """Main entry point for the chat interface"""
    try:
        chat_interface = ChatInterface()
        chat_interface.render_input_form()
        if st.session_state['generated']:
            chat_interface.render_chat_history()
    except Exception as e:
        logger.error(f"Application error: {e}")
        st.error("An unexpected error occurred. Please try again later.")

if __name__ == "__main__":
    main()