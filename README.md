# Talk to PDF 🤖📑

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://talk-to-pdf.streamlit.app/)

An AI-powered application that enables natural language interaction with PDF documents, leveraging OpenAI's language models and LlamaIndex for intelligent document processing.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Technical Architecture](#technical-architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Technical Documentation](#technical-documentation)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Overview

Talk to PDF transforms how users interact with PDF documents by enabling natural language conversations about document content. The application processes PDFs through an advanced pipeline of document indexing, vector storage creation, and context-aware response generation, allowing users to extract information through intuitive dialogue rather than manual searching.

### Key Benefits
- 🚀 Instant access to document content through natural language queries
- 🧠 Context-aware responses that understand document structure
- 📊 Efficient document indexing for quick information retrieval
- 🎯 User-friendly interface with progressive feature disclosure

## Features

### 1. Intelligent PDF Processing
- Advanced document processing using LlamaIndex and OpenAI embeddings
- Efficient temporary file handling and cleanup
- Support for multiple PDF documents
- Secure document processing pipeline

### 2. Context-Aware Question Answering
- Natural conversation flow with context retention
- Custom prompt templates for accurate responses
- Real-time response streaming
- Conversation history management

### 3. Flexible Configuration
- Choice between GPT-3.5 and GPT-4 models
- Adjustable temperature settings for response generation
- Customizable chat interface
- Session-based state management

## Technical Architecture

### System Components
```
talk_to_pdf/
├── 0_🔌API_KEY.py          # API configuration entry point
├── functions.py            # Shared utility functions
└── pages/
    ├── 1_📑UPLOAD_PDF.py   # Document processing
    └── 2_💬CHAT_WITH_PDF.py # Chat interface
```

### Technology Stack
- **Python 3.11**: Core programming language
- **Streamlit 1.38.0**: Web application framework
- **OpenAI 1.43.0**: Language models and embeddings
- **LlamaIndex 0.11.3**: Document processing and indexing
- **PyPDF 4.3.1**: PDF parsing and text extraction

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

3. Set up your OpenAI API key:
- Obtain an API key from [OpenAI Platform](https://platform.openai.com/account/api-keys)
- You'll enter this key when running the application

## Usage

1. Start the application:
```bash
streamlit run 0_🔌API_KEY.py
```

2. Enter your OpenAI API key when prompted

3. Upload your PDF document(s)

4. Start asking questions about your document content

## Technical Documentation

### Document Processing Pipeline

```python
def load_document(uploaded_files):
    temp_dir = tempfile.TemporaryDirectory()
    for file in uploaded_files:
        temp_filepath = os.path.join(temp_dir.name, file.name)
        with open(temp_filepath, "wb") as f:
            f.write(file.getvalue())
    reader = SimpleDirectoryReader(input_dir=temp_dir.name)
    return reader.load_data()
```

### Query Engine Configuration

```python
def query_engine(docs, model_name, temperature):    
    llm = OpenAI(model=model_name, temperature=temperature)
    Settings.llm = llm
    index = VectorStoreIndex.from_documents(docs, llm=llm)
    return index.as_query_engine()
```

### Chat Interface Implementation

```python
custom_prompt = PromptTemplate("""
Given a conversation (between Human and Assistant) and a follow up message from Human, 
rewrite the message to be a standalone question that captures all relevant context 
from the conversation.

<Chat History> 
{chat_history}

<Follow Up Message>
{question}

<Standalone question>
""")
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

Author: [Kaushal](https://twitter.com/holy_kau)

Project Link: [https://github.com/yourusername/talk-to-pdf](https://github.com/yourusername/talk-to-pdf)

---

Made with ❤️ by Kaushal | [Support my work](https://www.buymeacoffee.com/kaushal.ai)