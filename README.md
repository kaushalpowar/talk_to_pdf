# Talk to PDF 🤖📑

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://talk-to-pdf.streamlit.app/)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![OpenAI](https://img.shields.io/badge/OpenAI-API-orange.svg)](https://platform.openai.com/)

An innovative web application that enables natural language interaction with PDF documents through an AI-powered interface. Leveraging OpenAI's language models and LlamaIndex for document processing, Talk to PDF creates a seamless question-answering system for PDF content.

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

3. Run the application
```bash
streamlit run 0_🔌API_KEY.py
```

## 🏗️ System Architecture

The application follows a three-tier architecture with clear separation of concerns:

1. **Presentation Layer**: Streamlit-based user interface
2. **Processing Layer**: Document indexing and query processing
3. **Integration Layer**: OpenAI API integration and vector storage

### Component Structure
```
talk_to_pdf/
├── 0_🔌API_KEY.py          # API configuration entry point
├── functions.py            # Shared utility functions
└── pages/
    ├── 1_📑UPLOAD_PDF.py   # Document processing
    └── 2_💬CHAT_WITH_PDF.py # Chat interface
```

## 🎯 Key Features

### 1. Intelligent PDF Processing
- Advanced document indexing using LlamaIndex
- Efficient vector storage for quick retrieval
- Support for multiple PDF documents
- Secure temporary file handling

### 2. Context-Aware Question Answering
- Natural language query processing
- Conversation history management
- Dynamic context integration
- Real-time response streaming

### 3. User-Friendly Interface
- Step-by-step guided workflow
- Customizable model parameters
- Interactive chat interface
- Clear visual feedback

## 💻 Technical Implementation

### Document Processing
```python
def load_document(uploaded_files):
    """Process uploaded PDF files and create document index."""
    temp_dir = tempfile.TemporaryDirectory()
    for file in uploaded_files:
        temp_filepath = os.path.join(temp_dir.name, file.name)
        with open(temp_filepath, "wb") as f:
            f.write(file.getvalue())
    reader = SimpleDirectoryReader(input_dir=temp_dir.name)
    return reader.load_data()
```

### Chat Engine Configuration
```python
def setup_chat_engine(query_engine, custom_prompt, chat_history):
    """Configure context-aware chat engine with custom prompts."""
    return CondenseQuestionChatEngine.from_defaults(
        query_engine=query_engine,
        condense_question_prompt=custom_prompt,
        chat_history=chat_history
    )
```

## 🛠️ Technology Stack

- **Python**: Version 3.11
- **Streamlit**: Version 1.38.0 - Web framework
- **OpenAI**: Version 1.43.0 - Language models
- **LlamaIndex**: Version 0.11.3 - Document processing
- **Additional Extensions**:
  - streamlit-chat (0.1.1)
  - streamlit-extras (0.4.7)
  - markdownlit (0.0.7)

## 🔧 Configuration

### OpenAI API Setup
1. Obtain API key from [OpenAI Platform](https://platform.openai.com/account/api-keys)
2. Enter key in application's configuration page
3. Select preferred model (GPT-3.5-turbo or GPT-4)
4. Adjust temperature parameter (0.1-1.0)

### Document Processing Settings
- Supports multiple PDF uploads
- Automatic document indexing
- Vector store creation for efficient querying
- Session-based state management

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Contact

- **Author**: [Kaushal](https://twitter.com/holy_kau)
- **LinkedIn**: [Kaushal Powar](https://www.linkedin.com/in/kaushal-powar-a52b1a159/)
- **Project Link**: [GitHub Repository](https://github.com/yourusername/talk-to-pdf)

## 🙏 Acknowledgments

- OpenAI for providing powerful language models
- LlamaIndex team for document processing capabilities
- Streamlit for the excellent web framework

---

Made with ❤️ by Kaushal | [Support my work](https://www.buymeacoffee.com/kaushal.ai)