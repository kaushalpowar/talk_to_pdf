import streamlit as st
from streamlit_chat import message
from functions import sidebar_stuff3
from llama_index.core.prompts import PromptTemplate
from llama_index.core.chat_engine.condense_question import CondenseQuestionChatEngine
from llama_index.core.llms import ChatMessage, MessageRole

sidebar_stuff3()

query_engine = st.session_state['query_engine']
index = st.session_state['index']

# Custom prompt template for context-aware question reformulation
custom_prompt = PromptTemplate("""\
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

# Initialize chat engine with the query engine and custom prompt
chat_engine = CondenseQuestionChatEngine.from_defaults(
    query_engine=query_engine, 
    condense_question_prompt=custom_prompt,
    chat_history=custom_chat_history
)

# Function to handle conversational chat with streaming responses
def conversational_chat(query):
    streaming_response = chat_engine.stream_chat(query)
    response_tokens = []
    for token in streaming_response.response_gen:
        response_tokens.append(token)
    return ''.join(response_tokens)

# Initialize session state variables for chat history
if 'history' not in st.session_state:
    st.session_state['history'] = []

if 'generated' not in st.session_state:
    st.session_state['generated'] = ["Hello! Ask me anything about the uploaded document 🤗"]

if 'past' not in st.session_state:
    st.session_state['past'] = ["Hey! 👋"]

# Containers for chat history and user input
response_container = st.container()
container = st.container()

# User input form for querying the document
with container:
    with st.form(key='my_form', clear_on_submit=True):
        user_input = st.text_input("Query:", placeholder="What is this document about?", key='input')
        submit_button = st.form_submit_button(label='Send')
        
    # Handle user input and generate response
    if submit_button and user_input:
        output = conversational_chat(user_input)
        st.session_state['past'].append(user_input)
        st.session_state['generated'].append(output)

# Display chat history
if st.session_state['generated']:
    with response_container:
        for i in range(len(st.session_state['generated'])):
            message(st.session_state["past"][i], is_user=True, key=str(i) + '_user', avatar_style="big-ears", seed="missy")
            message(st.session_state["generated"][i], key=str(i))