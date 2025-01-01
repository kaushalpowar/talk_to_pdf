"""
Chat interface implementation for the Talk to PDF application.
Handles conversation management, prompt generation, and response streaming.
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

class PromptManager:
    """Manages prompt templates and chat history."""
    
    @staticmethod
    def get_default_prompt() -> PromptTemplate:
        """Returns the default prompt template for question condensing."""
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

    @staticmethod
    def get_initial_chat_history() -> List[ChatMessage]:
        """Returns the initial chat history."""
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

class ChatInterface:
    """Handles chat functionality and state management."""
    
    def __init__(self):
        """Initialize chat interface and state."""
        self.initialize_session_state()
        self.setup_chat_engine()
        
    def initialize_session_state(self):
        """Initialize or get session state variables."""
        if 'history' not in st.session_state:
            st.session_state['history'] = []
        if 'generated' not in st.session_state:
            st.session_state['generated'] = [DEFAULT_GREETING]
        if 'past' not in st.session_state:
            st.session_state['past'] = [DEFAULT_USER_GREETING]

    def setup_chat_engine(self):
        """Set up the chat engine with query engine and custom prompt."""
        try:
            self.query_engine = st.session_state['query_engine']
            self.index = st.session_state['index']
            
            self.chat_engine = CondenseQuestionChatEngine.from_defaults(
                query_engine=self.query_engine,
                condense_question_prompt=PromptManager.get_default_prompt(),
                chat_history=PromptManager.get_initial_chat_history()
            )
        except KeyError as e:
            st.error(f"Error initializing chat engine: {str(e)}")
            st.stop()

    def process_chat(self, user_input: str) -> str:
        """Process user input and generate response."""
        try:
            streaming_response = self.chat_engine.stream_chat(user_input)
            return ''.join(token for token in streaming_response.response_gen)
        except Exception as e:
            st.error(f"Error processing chat: {str(e)}")
            return "I apologize, but I encountered an error processing your request."

    def render_chat_interface(self):
        """Render the chat interface components."""
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
                output = self.process_chat(user_input)
                st.session_state['past'].append(user_input)
                st.session_state['generated'].append(output)

        self.render_chat_history(response_container)

    def render_chat_history(self, container):
        """Render chat history in the provided container."""
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
    """Main function to run the chat interface."""
    # Initialize sidebar
    sidebar_stuff3()
    
    # Initialize and render chat interface
    chat_interface = ChatInterface()
    chat_interface.render_chat_interface()

if __name__ == "__main__":
    main()