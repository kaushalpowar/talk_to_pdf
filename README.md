# Talk to PDF 🤖📑

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://talk-to-pdf.streamlit.app/)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![OpenAI](https://img.shields.io/badge/OpenAI-API-blue.svg)](https://openai.com/blog/openai-api)

An innovative AI-powered application that enables natural language interaction with PDF documents. Leveraging OpenAI's language models and LlamaIndex for document processing, Talk to PDF creates a seamless question-answering system for PDF content.

## 🌟 Features

- 📚 Natural language interaction with PDF documents
- 🤖 Powered by OpenAI's GPT models
- 📑 Efficient document indexing and retrieval
- 💬 Context-aware conversation system
- 🔄 Real-time response streaming
- 🎛️ Customizable model parameters

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- OpenAI API key
- Streamlit account (for deployment)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/talk-to-pdf.git
cd talk-to-pdf
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run 0_🔌API_KEY.py
```

## 🏗️ Architecture

The application follows a multi-page architecture with three primary components:

1. **API Configuration Interface** - Secure API key management
2. **Document Upload and Processing** - PDF handling and indexing
3. **Interactive Chat Interface** - Natural language interaction

```
talk_to_pdf/
├── 0_🔌API_KEY.py          # API configuration entry point
├── functions.py            # Shared utility functions
└── pages/
    ├── 1_📑UPLOAD_PDF.py   # Document processing
    └── 2_💬CHAT_WITH_PDF.py # Chat interface
```

## 💻 Technical Implementation

### Document Processing Engine

```python
def query_engine(docs, model_name, temperature):    
    llm = OpenAI(model=model_name, temperature=temperature)
    Settings.llm = llm
    index = VectorStoreIndex.from_documents(docs, llm=llm)
    query_engine = index.as_query_engine()
    return query_engine
```

### Context-Aware Chat System

```python
custom_prompt = PromptTemplate("""
Given a conversation (between Human and Assistant) and a follow up message from Human, \
rewrite the message to be a standalone question that captures all relevant context \
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
    streaming_response = chat_engine.stream_chat(query)
    response_tokens = []
    for token in streaming_response.response_gen:
        response_tokens.append(token)
    return ''.join(response_tokens)
```

## 🛠️ Technology Stack

- **Python** (3.11) - Core programming language
- **Streamlit** (1.38.0) - Web application framework
- **OpenAI** (1.43.0) - Natural language processing
- **LlamaIndex** (0.11.3) - Document processing and indexing
- **PyPDF** (4.3.1) - PDF handling

## 🌟 Key Benefits

1. **Enhanced Document Analysis**
   - Instant natural language querying
   - Context-aware responses
   - Efficient information retrieval

2. **User Experience**
   - Intuitive chat interface
   - Real-time response streaming
   - Customizable parameters

3. **Technical Advantages**
   - Scalable architecture
   - Efficient memory management
   - Secure document processing
   - Modular design

## 🔒 Security Considerations

- API keys are securely handled using password-masked inputs
- Temporary file handling for document processing
- Session-based state management
- Secure document cleanup after processing

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📬 Contact

Kaushal - [@holy_kau](https://twitter.com/holy_kau)

Project Link: [https://github.com/yourusername/talk-to-pdf](https://github.com/yourusername/talk-to-pdf)

## 🙏 Acknowledgments

- OpenAI for their powerful language models
- Streamlit team for the excellent framework
- LlamaIndex for document processing capabilities

---

Made with ❤️ by [Kaushal](https://twitter.com/holy_kau)