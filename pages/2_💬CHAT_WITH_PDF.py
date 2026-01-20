"""
Chat Interface Module for Talk to PDF application.
Implements a Streamlit-based chat interface with LlamaIndex integration for document Q&A.
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
    """Chat interface configuration settings."""
    INITIAL_GREETING: str = "Hello! Ask me anything about the uploaded document 🤗"
    INITIAL_USER_MSG: str = "Hey! 👋"
    QUERY_PLACEHOLDER: str = "What is this document about?"
    AVATAR_STYLE: str = "big-ears"
    AVATAR_SEED: str = "missy"

# Custom prompt template
CUSTOM_PROMPT = PromptTemplate("""
Given a conversation (between Human and Assistant) and a follow up message from Human, \
rewrite the message to be a standalone question that captures all relevant context \
from the conversation.

<Chat History> 
{chat_history}

<Follow Up Message>
{question}

<Standalone question>
""")

# Initial chat history
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
        st.session_state['generated'] = [ChatConfig.INITIAL_GREETING]
    if 'past' not in st.session_state:
        st.session_state['past'] = [ChatConfig.INITIAL_USER_MSG]

def setup_chat_engine() -> CondenseQuestionChatEngine:
    """Initialize and configure the chat engine."""
    try:
        query_engine = st.session_state['query_engine']
        return CondenseQuestionChatEngine.from_defaults(
            query_engine=query_engine,
            condense_question_prompt=CUSTOM_PROMPT,
            chat_history=INITIAL_CHAT_HISTORY
        )
    except KeyError:
        st.error("Query engine not found in session state. Please upload a document first.")
        st.stop()

def process_streaming_response(response_gen) -> str:
    """Process streaming response from chat engine."""
    try:
        return ''.join(token for token in response_gen)
    except Exception as e:
        st.error(f"Error processing response: {str(e)}")
        return "Sorry, I encountered an error processing your request."

def handle_user_input(chat_engine: CondenseQuestionChatEngine, user_input: str) -> None:
    """Process user input and generate response."""
    try:
        streaming_response = chat_engine.stream_chat(user_input)
        output = process_streaming_response(streaming_response.response_gen)
        
        st.session_state['past'].append(user_input)
        st.session_state['generated'].append(output)
    except Exception as e:
        st.error(f"Error generating response: {str(e)}")

def render_chat_history() -> None:
    """Render chat history using Streamlit message components."""
    with st.container():
        for i in range(len(st.session_state['generated'])):
            message(
                st.session_state["past"][i],
                is_user=True,
                key=f"{i}_user",
                avatar_style=ChatConfig.AVATAR_STYLE,
                seed=ChatConfig.AVATAR_SEED
            )
            message(st.session_state["generated"][i], key=str(i))

def render_input_form(chat_engine: CondenseQuestionChatEngine) -> None:
    """Render user input form."""
    with st.form(key='chat_form', clear_on_submit=True):
        user_input = st.text_input(
            "Query:",
            placeholder=ChatConfig.QUERY_PLACEHOLDER,
            key='input'
        )
        submit_button = st.form_submit_button(label='Send')
        
        if submit_button and user_input:
            handle_user_input(chat_engine, user_input)

def main():
    """Main function to run the chat interface."""
    # Setup sidebar
    sidebar_stuff3()
    
    # Initialize session state
    initialize_session_state()
    
    # Setup chat engine
    chat_engine = setup_chat_engine()
    
    # Initial greeting
    chat_engine.chat("Hello!")
    
    # Create chat interface containers
    response_container = st.container()
    input_container = st.container()
    
    # Render chat interface
    with input_container:
        render_input_form(chat_engine)
    
    with response_container:
        render_chat_history()

if __name__ == "__main__":
    main()