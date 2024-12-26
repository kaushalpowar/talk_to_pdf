# Talk to PDF 🤖📑

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://talk-to-pdf.streamlit.app/)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-311/)
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Technical Architecture](#technical-architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Components](#components)
- [Technology Stack](#technology-stack)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Overview

Talk to PDF is an innovative web application that enables natural language interaction with PDF documents through an AI-powered interface. The project leverages OpenAI's language models and LlamaIndex for document processing to create a seamless question-answering system for PDF content.

### Key Components
- API Configuration Interface
- Document Upload and Processing System
- Interactive Chat Interface

## Features

### 1. Intelligent PDF Processing
- Advanced document indexing using LlamaIndex
- Efficient vector storage creation
- Secure document handling
- Multiple PDF support

### 2. Context-Aware Question Answering
- Natural language understanding
- Conversation history management
- Context preservation across queries
- Real-time response streaming

### 3. User-Friendly Interface
- Step-by-step workflow
- Clear visual feedback
- Intuitive chat interface
- Customizable response parameters

## Technical Architecture

### Project Structure
```
talk_to_pdf/
├── 0_🔌API_KEY.py          # API configuration entry point
├── functions.py            # Shared utility functions
└── pages/
    ├── 1_📑UPLOAD_PDF.py   # Document processing
    └── 2_💬CHAT_WITH_PDF.py # Chat interface
```

### Core Components

#### 1. API Configuration Module
```python
def handle_api_key():
    api_key = st.text_input("Enter your OpenAI API key", type="password")
    st.session_state['api_key'] = api_key
    return api_key
```

#### 2. Document Processing Engine
```python
def query_engine(docs, model_name, temperature):    
    llm = OpenAI(model=model_name, temperature=temperature)
    index = VectorStoreIndex.from_documents(docs, llm=llm)
    return index.as_query_engine()
```

#### 3. Chat Interface System
```python
def conversational_chat(query):
    streaming_response = chat_engine.stream_chat(query)
    return ''.join(token for token in streaming_response.response_gen)
```

## Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/talk-to-pdf.git
cd talk-to-pdf
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Set up environment variables
```bash
export OPENAI_API_KEY=your_api_key_here
```

## Usage

1. Start the application
```bash
streamlit run 0_🔌API_KEY.py
```

2. Enter your OpenAI API key
3. Upload your PDF document
4. Start chatting with your document!

## Components

### 1. API Configuration
- Secure API key management
- Session state persistence
- Validation and error handling

### 2. Document Processing
- PDF text extraction
- Vector embedding generation
- Index creation and management

### 3. Chat Interface
- Real-time response streaming
- Context management
- History tracking
- Custom prompt templates

## Technology Stack

### Core Technologies
- **Python**: 3.11
- **Streamlit**: 1.38.0
- **OpenAI**: 1.43.0
- **LlamaIndex**: 0.11.3

### Key Dependencies
- **streamlit-chat**: 0.1.1
- **streamlit-extras**: 0.4.7
- **pypdf**: 4.3.1

### Development Tools
- **pip-compile** for dependency management
- **Git** for version control
- **Visual Studio Code** recommended IDE

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

Author: [Kaushal](https://www.linkedin.com/in/kaushal-powar-a52b1a159/)

Project Link: [https://github.com/yourusername/talk-to-pdf](https://github.com/yourusername/talk-to-pdf)

---

Made with ❤️ by Kaushal | [Twitter](https://twitter.com/holy_kau)