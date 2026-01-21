"""
Chat interface implementation using Streamlit and LlamaIndex for document Q&A.
Provides a conversational interface for querying document content with context awareness.
"""

import logging
from dataclasses import dataclass
from typing import List, Optional

import streamlit as st
from streamlit_chat import message
from llama_index.core.prompts import PromptTemplate
from llama_index.core.chat_engine.condense_question import CondenseQuestionChatEngine
from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.core.base.base_query_engine import BaseQueryEngine

from functions import sidebar_stuff3

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
DEFAULT_GREETING = "Hello! Ask me anything about the uploaded document 🤗"
DEFAULT_USER_GREETING = "Hey! 👋"
QUERY_PLACEHOLDER = "What is this document about?"

@dataclass
class ChatConfig:
    """Configuration for chat interface."""
    initial_system_prompt: str = """
    Hello assistant, given is a document. Please answer the question by understanding 
    the context and information of the document. Use your own knowledge and 
    understanding to answer the question.
    """
    temperature: float = 0.7
    max_tokens: int = 1500

class DocumentChatEngine:
    """Handles document chat functionality using LlamaIndex."""
    
    def __init__(self, query_engine: BaseQueryEngine, config: Optional[ChatConfig] = None):
        """Initialize chat engine with query engine and optional config."""
        self.query_engine = query_engine
        self.config = config or ChatConfig()
        self.chat_engine = self._initialize_chat_engine()

    def _initialize_chat_engine(self) -> CondenseQuestionChatEngine:
        """Set up the chat engine with custom prompt and history."""
        custom_prompt = PromptTemplate("""
            Given a conversation (between Human and Assistant) and a follow up message from Human, 
            rewrite the message to be a standalone question that captures all relevant context 
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
                content=self.config.initial_system_prompt
            ),
            ChatMessage(
                role=MessageRole.ASSISTANT,
                content='Okay, sounds good.'
            )
        ]

        return CondenseQuestionChatEngine.from_defaults(
            query_engine=self.query_engine,
            condense_question_prompt=custom_prompt,
            chat_history=custom_chat_history
        )

    async def get_response(self, query: str) -> str:
        """Get streaming response for user query."""
        try:
            streaming_response = self.chat_engine.stream_chat(query)
            response_tokens = []
            async for token in streaming_response.response_gen:
                response_tokens.append(token)
            return ''.join(response_tokens)
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return "I apologize, but I encountered an error processing your request."

class ChatInterface:
    """Handles Streamlit chat interface and state management."""

    def __init__(self):
        """Initialize chat interface and state."""
        self._initialize_session_state()
        self.chat_engine = self._setup_chat_engine()
        sidebar_stuff3()

    def _initialize_session_state(self):
        """Initialize Streamlit session state variables."""
        if 'history' not in st.session_state:
            st.session_state['history'] = []
        if 'generated' not in st.session_state:
            st.session_state['generated'] = [DEFAULT_GREETING]
        if 'past' not in st.session_state:
            st.session_state['past'] = [DEFAULT_USER_GREETING]

    def _setup_chat_engine(self) -> DocumentChatEngine:
        """Set up document chat engine from session state."""
        if 'query_engine' not in st.session_state:
            raise RuntimeError("Query engine not found in session state. Please upload a document first.")
        
        return DocumentChatEngine(
            query_engine=st.session_state['query_engine'],
            config=ChatConfig()
        )

    def render(self):
        """Render chat interface and handle user input."""
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
                self._handle_user_input(user_input)

        self._display_chat_history(response_container)

    def _handle_user_input(self, user_input: str):
        """Process user input and generate response."""
        output = self.chat_engine.get_response(user_input)
        st.session_state['past'].append(user_input)
        st.session_state['generated'].append(output)

    def _display_chat_history(self, container):
        """Display chat history in Streamlit container."""
        if st.session_state['generated']:
            with container:
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
    """Main entry point for chat interface."""
    try:
        chat_interface = ChatInterface()
        chat_interface.render()
    except Exception as e:
        logger.error(f"Error initializing chat interface: {e}")
        st.error("An error occurred while setting up the chat interface. Please ensure you've uploaded a document first.")

if __name__ == "__main__":
    main()