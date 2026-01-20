# Talk to PDF 🤖 📑️

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.38.0-red.svg)](https://streamlit.io/)
[![OpenAI](https://img.shields.io/badge/OpenAI-API-green.svg)](https://openai.com/api/)

An intelligent document interaction system that enables natural language conversations with PDF documents. Powered by OpenAI's language models and Streamlit, this application allows users to extract insights and information from PDFs through simple questions and answers.

## 🌟 Features

- Natural language interaction with PDF documents
- Real-time AI-powered responses
- Support for multiple PDF uploads
- Context-aware conversation handling
- Customizable AI model parameters
- User-friendly interface
- Secure API key management

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- OpenAI API key
- Internet connection

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/talk-to-pdf.git
cd talk-to-pdf
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Launch the application:
```bash
streamlit run app.py
```

## 📖 Usage Guide

### 1. API Key Setup
- Navigate to the application's home page
- Locate the "Enter your OpenAI API key" section
- Get your API key from [OpenAI Platform](https://platform.openai.com/account/api-keys)
- Enter the key in the secure input field
- Click "Submit" to save your API key

### 2. Document Upload
- Go to the PDF upload section
- Click "Browse Files" or drag and drop your PDF
- Support for multiple PDF uploads
- Wait for the indexing process to complete

### 3. Asking Questions
- Type your question in the input box
- Questions can be about any content within the uploaded PDF(s)
- Click "Ask" or press Enter to submit
- Receive AI-generated responses in real-time

### 4. Advanced Options
- Select between different GPT models (gpt-3.5-turbo or gpt-4)
- Adjust temperature settings for response variety
- View conversation history
- Start new conversations as needed

## 🛠️ Technical Details

- Built with Streamlit for the web interface
- Uses OpenAI's GPT models for natural language processing
- Implements LlamaIndex for document indexing and retrieval
- Features real-time response streaming
- Secure API key handling
- Session-based state management

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for:

- Bug fixes
- Feature additions
- Documentation improvements
- Performance optimizations

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built by [Kaushal](https://twitter.com/holy_kau)
- Powered by OpenAI's language models
- Made possible with Streamlit and LlamaIndex

## 📬 Contact & Support

- Author: Kaushal
- Twitter: [@holy_kau](https://twitter.com/holy_kau)
- Support the project: [Buy Me a Coffee](https://www.buymeacoffee.com/kaushal.ai)

---

Enjoy exploring your PDFs through natural conversation! 🚀📄