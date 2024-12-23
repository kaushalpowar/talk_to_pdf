# Talk to PDF 🤖📑

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://talk-to-pdf.streamlit.app/)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![OpenAI](https://img.shields.io/badge/OpenAI-API-blue.svg)](https://openai.com/blog/openai-api)

An innovative web application that enables natural language interaction with PDF documents through an AI-powered interface. Talk to PDF leverages OpenAI's language models and LlamaIndex for sophisticated document processing, creating a seamless question-answering system for PDF content.

## 🚀 Quick Start

1. Clone the repository
```bash
git clone https://github.com/yourusername/talk-to-pdf.git
cd talk-to-pdf
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Set up your OpenAI API key
```bash
export OPENAI_API_KEY='your-api-key'
```

4. Run the application
```bash
streamlit run 0_🔌API_KEY.py
```

## 🏗️ Architecture

The application follows a modular three-tier architecture:

```
talk_to_pdf/
├── 0_🔌API_KEY.py          # API configuration entry point
├── functions.py            # Shared utility functions
└── pages/
    ├── 1_📑UPLOAD_PDF.py   # Document processing
    └── 2_💬CHAT_WITH_PDF.py # Chat interface
```

### Core Components

1. **API Configuration Interface**
   - Secure API key management
   - Session state initialization
   - Environment validation

2. **Document Processing System**
   - PDF upload and validation
   - Document indexing using LlamaIndex
   - Vector store creation

3. **Interactive Chat Interface**
   - Context-aware conversations
   - Real-time response streaming
   - History management

## 💻 Technical Stack

### Core Technologies

- **Python 3.11**: Primary development language
- **Streamlit 1.38.0**: Web application framework
- **OpenAI API 1.43.0**: Natural language processing
- **LlamaIndex 0.11.3**: Document processing and indexing

### Key Dependencies

```txt
streamlit==1.38.0
openai==1.43.0
llama-index==0.11.3
pypdf==4.3.1
```

## 🔥 Features

### Intelligent PDF Processing

```python
def load_document(uploaded_files):
    """Process and load PDF documents for indexing."""
    temp_dir = tempfile.TemporaryDirectory()
    for file in uploaded_files:
        temp_filepath = os.path.join(temp_dir.name, file.name)
        with open(temp_filepath, "wb") as f:
            f.write(file.getvalue())
    reader = SimpleDirectoryReader(input_dir=temp_dir.name)
    return reader.load_data()
```

### Context-Aware Conversations

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

### Real-Time Response Streaming

```python
def conversational_chat(query):
    """Stream responses in real-time for better user experience."""
    streaming_response = chat_engine.stream_chat(query)
    return ''.join(token for token in streaming_response.response_gen)
```

## 🎯 Benefits

1. **Enhanced Efficiency**
   - Natural language document querying
   - Context-aware response generation
   - Quick information retrieval

2. **User-Friendly Design**
   - Intuitive step-by-step interface
   - Clear visual feedback
   - Customizable response parameters

3. **Technical Advantages**
   - Scalable architecture
   - Efficient memory management
   - Secure document processing
   - Modular component design

## 🛠️ Development

### Prerequisites

- Python 3.11+
- OpenAI API key
- Git

### Local Development Setup

1. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Unix
venv\Scripts\activate     # Windows
```

2. Install development dependencies
```bash
pip install -r requirements-dev.txt
```

3. Set up pre-commit hooks
```bash
pre-commit install
```

### Running Tests

```bash
pytest tests/
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📬 Contact

Kaushal - [@holy_kau](https://twitter.com/holy_kau)

Project Link: [https://github.com/yourusername/talk-to-pdf](https://github.com/yourusername/talk-to-pdf)

## 🙏 Acknowledgments

- OpenAI for their powerful language models
- LlamaIndex for document processing capabilities
- Streamlit for the excellent web framework

---

Made with ❤️ by [Kaushal](https://www.linkedin.com/in/kaushal-powar-a52b1a159/)