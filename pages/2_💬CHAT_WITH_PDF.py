"""
Chat Interface Module for PDF Question-Answering System
Implements a Streamlit-based chat interface using LlamaIndex for document Q&A.
"""

from typing import List, Optional, Dict, Any

import streamlit as st
from streamlit_chat import message
from llama_index.core.prompts import PromptTemplate
from llama_index.core.chat_engine.condense_question import CondenseQuestionChatEngine
from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.core.base.base_query_engine import BaseQueryEngine

from functions import sidebar_stuff3

# Configuration
INITIAL_GREETING = "Hello! Ask me anything about the uploaded document 🤗"
INITIAL_USER_MSG = "Hey! 👋"
AVATAR_STYLE = "big-ears"
AVATAR_SEED = "missy"

class ChatConfig:
    """Configuration for the chat interface"""
    prompt_template = PromptTemplate("""
        Given a conversation (between Human and Assistant) and a follow up message from Human, \
        rewrite the message to be a standalone question that captures all relevant context \
        from the conversation.

        <Chat History> 
        {chat_history}

        <Follow Up Message>
        {question}

        <Standalone question>
    """)

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

class ChatInterface:
    """Manages the chat interface and conversation logic"""
    
    def __init__(self, query_engine: BaseQueryEngine):
        """Initialize chat interface with query engine"""
        self.query_engine = query_engine
        self.chat_engine = self._initialize_chat_engine()
        self._initialize_session_state()
        
    def _initialize_chat_engine(self) -> CondenseQuestionChatEngine:
        """Initialize the chat engine with custom configuration"""
        return CondenseQuestionChatEngine.from_defaults(
            query_engine=self.query_engine,
            condense_question_prompt=ChatConfig.prompt_template,
            chat_history=ChatConfig.initial_chat_history
        )
    
    def _initialize_session_state(self):
        """Initialize Streamlit session state variables"""
        if 'history' not in st.session_state:
            st.session_state['history'] = []
        if 'generated' not in st.session_state:
            st.session_state['generated'] = [INITIAL_GREETING]
        if 'past' not in st.session_state:
            st.session_state['past'] = [INITIAL_USER_MSG]
    
    def process_query(self, query: str) -> str:
        """Process user query and return response"""
        try:
            streaming_response = self.chat_engine.stream_chat(query)
            return ''.join(streaming_response.response_gen)
        except Exception as e:
            st.error(f"Error processing query: {str(e)}")
            return "I apologize, but I encountered an error processing your query. Please try again."
    
    def render_chat_interface(self):
        """Render the chat interface"""
        response_container = st.container()
        input_container = st.container()
        
        with input_container:
            with st.form(key='chat_form', clear_on_submit=True):
                user_input = st.text_input(
                    "Query:",
                    placeholder="What is this document about?",
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
                        avatar_style=AVATAR_STYLE,
                        seed=AVATAR_SEED
                    )
                    message(st.session_state["generated"][i], key=str(i))

def main():
    """Main application entry point"""
    # Initialize sidebar
    sidebar_stuff3()
    
    # Get query engine from session state
    try:
        query_engine = st.session_state['query_engine']
        index = st.session_state['index']  # Keep for compatibility
    except KeyError:
        st.error("Please upload a document first!")
        return
    
    # Initialize and render chat interface
    chat_interface = ChatInterface(query_engine)
    chat_interface.render_chat_interface()

if __name__ == "__main__":
    main()