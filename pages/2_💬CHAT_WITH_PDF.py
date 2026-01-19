"""
Chat interface implementation for PDF question-answering system using Streamlit and LlamaIndex.
Provides an interactive chat UI with context-aware responses based on uploaded PDF content.
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

# Prompt template for context-aware question reformulation
QUESTION_PROMPT = PromptTemplate("""
Given a conversation (between Human and Assistant) and a follow up message from Human, \
rewrite the message to be a standalone question that captures all relevant context \
from the conversation.

<Chat History> 
{chat_history}

<Follow Up Message>
{question}

<Standalone question>
""")

# Initial chat history to set context
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

def initialize_session_state() -> None:
    """Initialize Streamlit session state variables for chat history."""
    if 'history' not in st.session_state:
        st.session_state['history'] = []
    if 'generated' not in st.session_state:
        st.session_state['generated'] = [INITIAL_GREETING]
    if 'past' not in st.session_state:
        st.session_state['past'] = [INITIAL_USER_MSG]

def setup_chat_engine() -> CondenseQuestionChatEngine:
    """Initialize and configure the chat engine with the query engine from session state."""
    try:
        query_engine = st.session_state['query_engine']
        chat_engine = CondenseQuestionChatEngine.from_defaults(
            query_engine=query_engine,
            condense_question_prompt=QUESTION_PROMPT,
            chat_history=INITIAL_CHAT_HISTORY
        )
        return chat_engine
    except KeyError as e:
        logger.error(f"Failed to initialize chat engine: {e}")
        st.error("Error: Query engine not found in session state. Please upload a document first.")
        st.stop()

def process_chat_response(query: str, chat_engine: CondenseQuestionChatEngine) -> str:
    """Process user query and generate response using streaming."""
    try:
        streaming_response = chat_engine.stream_chat(query)
        response_tokens = []
        for token in streaming_response.response_gen:
            response_tokens.append(token)
        return ''.join(response_tokens)
    except Exception as e:
        logger.error(f"Error processing chat response: {e}")
        return "I apologize, but I encountered an error processing your question. Please try again."

def update_chat_history(user_input: str, response: str) -> None:
    """Update session state with new messages."""
    st.session_state['past'].append(user_input)
    st.session_state['generated'].append(response)

def render_chat_history() -> None:
    """Render the chat history using Streamlit chat messages."""
    with st.container():
        for i in range(len(st.session_state['generated'])):
            message(
                st.session_state["past"][i],
                is_user=True,
                key=f"{i}_user",
                avatar_style="big-ears",
                seed="missy"
            )
            message(st.session_state["generated"][i], key=str(i))

def render_chat_interface() -> None:
    """Render the chat interface with input form."""
    with st.container():
        with st.form(key='chat_form', clear_on_submit=True):
            user_input = st.text_input(
                "Query:",
                placeholder=QUERY_PLACEHOLDER,
                key='input'
            )
            submit_button = st.form_submit_button(label='Send')

        if submit_button and user_input:
            chat_engine = setup_chat_engine()
            response = process_chat_response(user_input, chat_engine)
            update_chat_history(user_input, response)

def main():
    """Main function to run the chat interface."""
    # Setup sidebar
    sidebar_stuff3()
    
    # Initialize session state
    initialize_session_state()
    
    # Initial chat engine setup
    chat_engine = setup_chat_engine()
    
    # Send initial greeting
    if not st.session_state['history']:
        chat_engine.chat("Hello!")
    
    # Render chat components
    render_chat_interface()
    if st.session_state['generated']:
        render_chat_history()

if __name__ == "__main__":
    main()