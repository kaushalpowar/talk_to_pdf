"""
Chat interface implementation for the Talk to PDF application.
Handles conversation management, prompt generation, and response streaming.
"""

import streamlit as st
from streamlit_chat import message
from typing import List, Optional
from dataclasses import dataclass
from functions import sidebar_stuff3
from llama_index.core.prompts import PromptTemplate
from llama_index.core.chat_engine.condense_question import CondenseQuestionChatEngine
from llama_index.core.llms import ChatMessage, MessageRole

# Constants
DEFAULT_GREETING = "Hello! Ask me anything about the uploaded document 🤗"
DEFAULT_USER_GREETING = "Hey! 👋"
QUERY_PLACEHOLDER = "What is this document about?"

# Custom prompt template
CHAT_PROMPT_TEMPLATE = """\
Given a conversation (between Human and Assistant) and a follow up message from Human, \
rewrite the message to be a standalone question that captures all relevant context \
from the conversation.

<Chat History> 
{chat_history}

<Follow Up Message>
{question}

<Standalone question>
"""

@dataclass
class ChatState:
    """Manages chat session state"""
    history: List[str]
    generated: List[str]
    past: List[str]

class PDFChatInterface:
    """Handles PDF chat functionality and UI rendering"""
    
    def __init__(self):
        self.query_engine = st.session_state.get('query_engine')
        self.index = st.session_state.get('index')
        self.chat_engine = self._initialize_chat_engine()
        self.state = self._initialize_state()
        
    def _initialize_chat_engine(self) -> CondenseQuestionChatEngine:
        """Initialize the chat engine with custom prompt and history"""
        custom_prompt = PromptTemplate(CHAT_PROMPT_TEMPLATE)
        
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
        
        return CondenseQuestionChatEngine.from_defaults(
            query_engine=self.query_engine,
            condense_question_prompt=custom_prompt,
            chat_history=initial_chat_history
        )
    
    def _initialize_state(self) -> ChatState:
        """Initialize or retrieve chat session state"""
        if 'history' not in st.session_state:
            st.session_state['history'] = []
        if 'generated' not in st.session_state:
            st.session_state['generated'] = [DEFAULT_GREETING]
        if 'past' not in st.session_state:
            st.session_state['past'] = [DEFAULT_USER_GREETING]
            
        return ChatState(
            history=st.session_state['history'],
            generated=st.session_state['generated'],
            past=st.session_state['past']
        )
    
    def _handle_chat_response(self, user_input: str) -> str:
        """Process user input and generate response"""
        try:
            streaming_response = self.chat_engine.stream_chat(user_input)
            response_tokens = []
            
            # Stream response tokens
            for token in streaming_response.response_gen:
                response_tokens.append(token)
                
            return ''.join(response_tokens)
        except Exception as e:
            st.error(f"Error generating response: {str(e)}")
            return "I apologize, but I encountered an error processing your request."
    
    def render_chat_interface(self):
        """Render the chat interface components"""
        # Create containers for chat layout
        response_container = st.container()
        input_container = st.container()
        
        # Render input form
        with input_container:
            with st.form(key='chat_form', clear_on_submit=True):
                user_input = st.text_input(
                    "Query:",
                    placeholder=QUERY_PLACEHOLDER,
                    key='input'
                )
                submit_button = st.form_submit_button(label='Send')
                
                if submit_button and user_input:
                    output = self._handle_chat_response(user_input)
                    self.state.past.append(user_input)
                    self.state.generated.append(output)
                    
                    # Update session state
                    st.session_state['past'] = self.state.past
                    st.session_state['generated'] = self.state.generated
        
        # Display chat history
        if self.state.generated:
            with response_container:
                for i in range(len(self.state.generated)):
                    message(
                        self.state.past[i],
                        is_user=True,
                        key=f"{i}_user",
                        avatar_style="big-ears",
                        seed="missy"
                    )
                    message(self.state.generated[i], key=str(i))

def main():
    """Main entry point for the chat interface"""
    # Initialize sidebar
    sidebar_stuff3()
    
    # Initialize and render chat interface
    chat_interface = PDFChatInterface()
    chat_interface.render_chat_interface()

if __name__ == "__main__":
    main()