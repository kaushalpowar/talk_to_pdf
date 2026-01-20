"""
Chat interface implementation for Talk to PDF application.
Handles conversation flow, document Q&A, and UI rendering using Streamlit and LlamaIndex.
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

class ChatState:
    """Manages chat session state."""
    
    def __init__(self):
        if 'history' not in st.session_state:
            st.session_state['history'] = []
        if 'generated' not in st.session_state:
            st.session_state['generated'] = [DEFAULT_GREETING]
        if 'past' not in st.session_state:
            st.session_state['past'] = [DEFAULT_USER_GREETING]
            
    def add_message(self, user_input: str, generated_output: str):
        """Add a message pair to chat history."""
        st.session_state['past'].append(user_input)
        st.session_state['generated'].append(generated_output)

class ChatEngine:
    """Handles chat engine configuration and response generation."""
    
    def __init__(self, query_engine):
        self.query_engine = query_engine
        self.chat_engine = self._configure_chat_engine()
        
    def _configure_chat_engine(self) -> CondenseQuestionChatEngine:
        """Configure the chat engine with custom prompt and history."""
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

        return CondenseQuestionChatEngine.from_defaults(
            query_engine=self.query_engine,
            condense_question_prompt=custom_prompt,
            chat_history=custom_chat_history
        )

    def get_response(self, query: str) -> str:
        """Generate streaming response for user query."""
        try:
            streaming_response = self.chat_engine.stream_chat(query)
            response_tokens = []
            for token in streaming_response.response_gen:
                response_tokens.append(token)
            return ''.join(response_tokens)
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return "I apologize, but I encountered an error processing your request. Please try again."

class ChatInterface:
    """Manages chat interface rendering and user interactions."""
    
    def __init__(self):
        sidebar_stuff3()
        self.state = ChatState()
        self.chat_engine = ChatEngine(st.session_state['query_engine'])
        
    def render_chat_history(self):
        """Render chat message history."""
        with st.container() as response_container:
            for i in range(len(st.session_state['generated'])):
                message(
                    st.session_state["past"][i],
                    is_user=True,
                    key=f"{i}_user",
                    avatar_style=AVATAR_STYLE,
                    seed=AVATAR_SEED
                )
                message(st.session_state["generated"][i], key=str(i))

    def render_input_form(self):
        """Render user input form and handle submissions."""
        with st.container() as container:
            with st.form(key='my_form', clear_on_submit=True):
                user_input = st.text_input(
                    "Query:",
                    placeholder="What is this document about?",
                    key='input'
                )
                submit_button = st.form_submit_button(label='Send')

            if submit_button and user_input:
                output = self.chat_engine.get_response(user_input)
                self.state.add_message(user_input, output)

def main():
    """Main application entry point."""
    try:
        chat_interface = ChatInterface()
        chat_interface.render_chat_history()
        chat_interface.render_input_form()
    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        st.error("An unexpected error occurred. Please refresh the page and try again.")

if __name__ == "__main__":
    main()