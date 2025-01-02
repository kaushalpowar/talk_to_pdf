"""
Chat Interface Module for Talk to PDF application.
Implements a conversational interface for document question-answering using LlamaIndex and Streamlit.
"""

from typing import List, Optional

import streamlit as st
from streamlit_chat import message
from llama_index.core.prompts import PromptTemplate
from llama_index.core.chat_engine.condense_question import CondenseQuestionChatEngine
from llama_index.core.llms import ChatMessage, MessageRole

from functions import sidebar_stuff3

# Constants
DEFAULT_GREETING = "Hello! Ask me anything about the uploaded document 🤗"
DEFAULT_USER_GREETING = "Hey! 👋"
QUERY_PLACEHOLDER = "What is this document about?"

# Prompt Templates
CONDENSE_QUESTION_PROMPT = PromptTemplate("""
Given a conversation (between Human and Assistant) and a follow up message from Human, \
rewrite the message to be a standalone question that captures all relevant context \
from the conversation.

<Chat History> 
{chat_history}

<Follow Up Message>
{question}

<Standalone question>
""")

# Initial chat history setup
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
    """Initialize Streamlit session state variables."""
    if 'history' not in st.session_state:
        st.session_state['history'] = []
    if 'generated' not in st.session_state:
        st.session_state['generated'] = [DEFAULT_GREETING]
    if 'past' not in st.session_state:
        st.session_state['past'] = [DEFAULT_USER_GREETING]

def setup_chat_engine() -> CondenseQuestionChatEngine:
    """Initialize and configure the chat engine."""
    try:
        query_engine = st.session_state['query_engine']
        return CondenseQuestionChatEngine.from_defaults(
            query_engine=query_engine,
            condense_question_prompt=CONDENSE_QUESTION_PROMPT,
            chat_history=INITIAL_CHAT_HISTORY
        )
    except KeyError:
        st.error("Query engine not found in session state. Please upload a document first.")
        st.stop()

def process_chat_response(query: str, chat_engine: CondenseQuestionChatEngine) -> str:
    """Process chat query and return response."""
    try:
        streaming_response = chat_engine.stream_chat(query)
        return ''.join(token for token in streaming_response.response_gen)
    except Exception as e:
        st.error(f"Error processing chat response: {str(e)}")
        return "I apologize, but I encountered an error processing your request."

def display_chat_history() -> None:
    """Display chat history using Streamlit chat messages."""
    if st.session_state['generated']:
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

def chat_interface() -> None:
    """Main chat interface implementation."""
    # Initialize session state and sidebar
    initialize_session_state()
    sidebar_stuff3()
    
    # Setup chat engine
    chat_engine = setup_chat_engine()
    
    # Initialize response containers
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
            output = process_chat_response(user_input, chat_engine)
            st.session_state['past'].append(user_input)
            st.session_state['generated'].append(output)
    
    # Display chat history
    with response_container:
        display_chat_history()

if __name__ == "__main__":
    chat_interface()