"""
Chat Interface Module for PDF Question-Answering System

This module implements a Streamlit-based chat interface that allows users to interact
with PDF documents using natural language queries. It uses LlamaIndex for document
processing and query handling.
"""

import streamlit as st
from streamlit_chat import message
from typing import List, Optional
from dataclasses import dataclass
from llama_index.core.prompts import PromptTemplate
from llama_index.core.chat_engine.condense_question import CondenseQuestionChatEngine
from llama_index.core.llms import ChatMessage, MessageRole
from functions import sidebar_stuff3

# Configuration
@dataclass
class ChatConfig:
    """Configuration settings for the chat interface."""
    INITIAL_GREETING: str = "Hello! Ask me anything about the uploaded document 🤗"
    INITIAL_USER_MSG: str = "Hey! 👋"
    QUERY_PLACEHOLDER: str = "What is this document about?"
    AVATAR_STYLE: str = "big-ears"
    AVATAR_SEED: str = "missy"

class ChatEngine:
    """Handles the setup and management of the LlamaIndex chat engine."""
    
    def __init__(self, query_engine, index):
        self.query_engine = query_engine
        self.index = index
        self.chat_engine = self._setup_chat_engine()

    def _get_custom_prompt(self) -> PromptTemplate:
        """Creates the custom prompt template for context-aware responses."""
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

    def _get_initial_chat_history(self) -> List[ChatMessage]:
        """Sets up the initial chat history with context."""
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

    def _setup_chat_engine(self) -> CondenseQuestionChatEngine:
        """Initializes the chat engine with custom configuration."""
        return CondenseQuestionChatEngine.from_defaults(
            query_engine=self.query_engine,
            condense_question_prompt=self._get_custom_prompt(),
            chat_history=self._get_initial_chat_history()
        )

    def get_response(self, query: str) -> str:
        """Generates a response for the given query using streaming."""
        streaming_response = self.chat_engine.stream_chat(query)
        return ''.join(token for token in streaming_response.response_gen)

class ChatInterface:
    """Manages the Streamlit chat interface and session state."""
    
    def __init__(self, config: ChatConfig):
        self.config = config
        self._initialize_session_state()
        self.chat_engine = ChatEngine(
            st.session_state['query_engine'],
            st.session_state['index']
        )

    def _initialize_session_state(self):
        """Initializes or retrieves session state variables."""
        if 'history' not in st.session_state:
            st.session_state['history'] = []
        if 'generated' not in st.session_state:
            st.session_state['generated'] = [self.config.INITIAL_GREETING]
        if 'past' not in st.session_state:
            st.session_state['past'] = [self.config.INITIAL_USER_MSG]

    def _render_chat_history(self):
        """Renders the chat history using Streamlit messages."""
        with st.container() as response_container:
            for i in range(len(st.session_state['generated'])):
                message(
                    st.session_state["past"][i],
                    is_user=True,
                    key=f"{i}_user",
                    avatar_style=self.config.AVATAR_STYLE,
                    seed=self.config.AVATAR_SEED
                )
                message(st.session_state["generated"][i], key=str(i))

    def _handle_user_input(self, user_input: str):
        """Processes user input and generates response."""
        output = self.chat_engine.get_response(user_input)
        st.session_state['past'].append(user_input)
        st.session_state['generated'].append(output)

    def render(self):
        """Renders the complete chat interface."""
        # Setup sidebar
        sidebar_stuff3()

        # Create input form
        with st.container() as container:
            with st.form(key='my_form', clear_on_submit=True):
                user_input = st.text_input(
                    "Query:",
                    placeholder=self.config.QUERY_PLACEHOLDER,
                    key='input'
                )
                submit_button = st.form_submit_button(label='Send')

            if submit_button and user_input:
                self._handle_user_input(user_input)

        # Display chat history
        if st.session_state['generated']:
            self._render_chat_history()

def main():
    """Main entry point for the chat interface."""
    config = ChatConfig()
    chat_interface = ChatInterface(config)
    chat_interface.render()

if __name__ == "__main__":
    main()