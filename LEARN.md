# Talk to PDF 🤖 📑️

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-311/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.38.0-FF4B4B.svg)](https://streamlit.io)
[![OpenAI](https://img.shields.io/badge/OpenAI-1.43.0-412991.svg)](https://openai.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An intelligent document interaction system that enables natural language conversations with PDF documents using state-of-the-art AI technology. Ask questions about your PDFs and receive instant, context-aware responses powered by OpenAI's language models.

## ✨ Features

- 📚 Support for multiple PDF documents
- 💬 Natural language question-answering
- 🔍 Context-aware responses
- ⚡ Real-time response streaming
- 🎛️ Configurable AI model parameters
- 🔒 Secure API key management
- 📱 Responsive web interface

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
streamlit run 0_🔌API_KEY.py
```

## 📖 Usage Guide

### 1. API Key Setup
- Navigate to the application's home page
- Enter your OpenAI API key in the secure input field
- Click "Submit" to save your API key
- Note: Get your API key from [OpenAI Platform](https://platform.openai.com/account/api-keys)

### 2. Document Upload
- Click "Browse Files" to select your PDF document(s)
- Support for single or multiple PDF files
- Wait for document processing and indexing

### 3. Ask Questions
- Type your question in the chat input box
- Click "Send" or press Enter
- Receive AI-generated responses based on document content
- Continue the conversation naturally with follow-up questions

### 4. Advanced Options
- Select between GPT-3.5 Turbo or GPT-4 models
- Adjust temperature settings for response variety
- View conversation history
- Clear chat or start new sessions

## 🛠️ Technical Architecture

- **Frontend**: Streamlit web framework
- **Document Processing**: LlamaIndex
- **Language Model**: OpenAI GPT models
- **Vector Storage**: Efficient document indexing
- **State Management**: Streamlit session state

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

Created with ❤️ by [Kaushal](https://twitter.com/holy_kau)

## 🙏 Acknowledgments

- OpenAI for their powerful language models
- Streamlit team for the amazing framework
- LlamaIndex for document processing capabilities
- All contributors and users of this project

---

Enjoy interacting with your PDFs using natural language! 🚀📄

For issues, feature requests, or questions, please [open an issue](https://github.com/yourusername/talk-to-pdf/issues) or reach out on Twitter [@holy_kau](https://twitter.com/holy_kau).