# Talk to PDF 🤖📑

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://talk-to-pdf.streamlit.app/)

An AI-powered application that enables natural language interaction with PDF documents through an intuitive chat interface.

## 📚 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Technical Architecture](#technical-architecture)
- [Implementation Details](#implementation-details)
- [Development](#development)
- [License](#license)
- [Contact](#contact)

## Overview

Talk to PDF leverages OpenAI's language models and LlamaIndex for sophisticated document processing, creating a seamless question-answering system for PDF content. The application follows a multi-page architecture built on Streamlit:

1. API Configuration Interface
2. Document Upload and Processing System
3. Interactive Chat Interface

## Features

### 🔍 Intelligent PDF Processing
- Advanced document indexing using LlamaIndex
- Efficient vector storage for quick retrieval
- Support for multiple PDF documents

### 💡 Context-Aware Question Answering
- Natural language query processing
- Conversation history management
- Contextual response generation

### ⚡ Real-Time Interaction
- Streaming responses for immediate feedback
- Progressive document processing
- Interactive chat interface

### 🎛️ Customization Options
- Multiple language model selection (GPT-3.5, GPT-4)
- Adjustable response parameters
- Configurable processing settings

## Prerequisites

- Python 3.11+
- OpenAI API key
- Streamlit account (for deployment)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/talk-to-pdf.git
cd talk-to-pdf
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. **Configure API Key**
```python
# Launch the application
streamlit run 0_🔌API_KEY.py
```

2. **Upload Documents**
- Select PDF files through the upload interface
- Configure model parameters (temperature, model selection)

3. **Start Chatting**
- Ask questions about your documents
- Receive AI-powered responses
- Maintain conversation context

## Technical Architecture

### Component Structure
```
talk_to_pdf/
├── 0_🔌API_KEY.py          # API configuration
├── functions.py            # Shared utilities
└── pages/
    ├── 1_📑UPLOAD_PDF.py   # Document processing
    └── 2_💬CHAT_WITH_PDF.py # Chat interface
```

### Core Technologies

#### Streamlit (v1.38.0)
```python
st.set_page_config(page_title="Talk to PDF", page_icon=":robot_face:", layout="wide")
st.title("Talk to your PDF 🤖 📑️")
```

#### LlamaIndex (v0.11.3)
```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

def create_index(docs):
    index = VectorStoreIndex.from_documents(docs)
    return index.as_query_engine()
```

#### OpenAI Integration (v1.43.0)
```python
def initialize_llm(model_name="gpt-3.5-turbo", temperature=0.5):
    return OpenAI(model=model_name, temperature=temperature)
```

## Implementation Details

### Document Processing
```python
def process_document(uploaded_files):
    with tempfile.TemporaryDirectory() as temp_dir:
        for file in uploaded_files:
            temp_filepath = os.path.join(temp_dir, file.name)
            with open(temp_filepath, "wb") as f:
                f.write(file.getvalue())
        
        reader = SimpleDirectoryReader(input_dir=temp_dir)
        return reader.load_data()
```

### Chat Engine Configuration
```python
def configure_chat_engine(query_engine, custom_prompt, chat_history):
    return CondenseQuestionChatEngine.from_defaults(
        query_engine=query_engine,
        condense_question_prompt=custom_prompt,
        chat_history=chat_history
    )
```

### State Management
```python
def initialize_session_state():
    if 'history' not in st.session_state:
        st.session_state['history'] = []
    if 'generated' not in st.session_state:
        st.session_state['generated'] = ["Hello! Ask me anything about the uploaded document 🤗"]
    if 'past' not in st.session_state:
        st.session_state['past'] = ["Hey! 👋"]
```

## Development

### Environment Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows

# Install development dependencies
pip install -r requirements-dev.txt
```

### Running Tests
```bash
pytest tests/
```

### Code Style
The project follows PEP 8 guidelines. Use pre-commit hooks for consistent formatting:
```bash
pre-commit install
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

- Author: [Kaushal](https://www.linkedin.com/in/kaushal-powar-a52b1a159/)
- Twitter: [@holy_kau](https://twitter.com/holy_kau)
- Project Link: [https://github.com/yourusername/talk-to-pdf](https://github.com/yourusername/talk-to-pdf)

---

Enjoy interacting with your PDFs using natural language! 🚀📄