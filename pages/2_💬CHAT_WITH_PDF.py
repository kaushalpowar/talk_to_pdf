"""
Chat Interface Module for PDF Question-Answering System

This module implements an interactive chat interface using Streamlit and LlamaIndex
for document-based question answering. It maintains conversation history and provides
streaming responses based on document context.
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

# Custom prompt template for context-aware question answering
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

def initialize_chat_engine() -> CondenseQuestionChatEngine:
    """
    Initialize the chat engine with custom prompt and chat history.
    
    Returns:
        CondenseQuestionChatEngine: Configured chat engine instance
    """
    try:
        query_engine = st.session_state['query_engine']
        custom_prompt = PromptTemplate(CUSTOM_PROMPT_TEMPLATE)
        
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
        
        chat_engine = CondenseQuestionChatEngine.from_defaults(
            query_engine=query_engine,
            condense_question_prompt=custom_prompt,
            chat_history=initial_chat_history
        )
        
        return chat_engine
    except Exception as e:
        logger.error(f"Failed to initialize chat engine: {str(e)}")
        raise

def process_chat_response(query: str, chat_engine: CondenseQuestionChatEngine) -> str:
    """
    Process user query and generate response using streaming.
    
    Args:
        query: User input query
        chat_engine: Initialized chat engine instance
    
    Returns:
        str: Generated response
    """
    try:
        streaming_response = chat_engine.stream_chat(query)
        response_tokens = []
        for token in streaming_response.response_gen:
            response_tokens.append(token)
        return ''.join(response_tokens)
    except Exception as e:
        logger.error(f"Error processing chat response: {str(e)}")
        return "I apologize, but I encountered an error processing your question. Please try again."

def initialize_session_state():
    """Initialize Streamlit session state variables if they don't exist."""
    if 'history' not in st.session_state:
        st.session_state['history'] = []
    if 'generated' not in st.session_state:
        st.session_state['generated'] = [DEFAULT_GREETING]
    if 'past' not in st.session_state:
        st.session_state['past'] = [DEFAULT_USER_GREETING]

def display_chat_history():
    """Display the chat history using Streamlit chat messages."""
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

def main():
    """Main function to run the chat interface."""
    # Initialize sidebar
    sidebar_stuff3()
    
    # Ensure required session state exists
    if 'query_engine' not in st.session_state or 'index' not in st.session_state:
        st.error("Please upload a document first!")
        return
    
    # Initialize chat components
    initialize_session_state()
    chat_engine = initialize_chat_engine()
    
    # Create chat interface
    with st.container() as input_container:
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
    if st.session_state['generated']:
        display_chat_history()

if __name__ == "__main__":
    main()