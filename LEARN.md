# Talk to PDF 🤖 📑️

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.38.0-FF4B4B.svg)](https://streamlit.io)
[![OpenAI](https://img.shields.io/badge/OpenAI-1.43.0-412991.svg)](https://openai.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An intelligent document interaction system that enables natural language conversations with PDF documents. Powered by OpenAI's language models and built with Streamlit, this application allows users to extract insights and information from PDFs through simple questions and answers.

## Features

- 🔍 Natural language querying of PDF documents
- 🤖 AI-powered context-aware responses
- 📚 Support for multiple PDF documents
- 🔄 Real-time streaming responses
- 🎛️ Configurable AI model parameters
- 💬 Interactive chat interface
- 🔒 Secure API key management

## Requirements

- Python 3.11+
- OpenAI API key
- Required Python packages (see `requirements.txt`)

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

3. Run the application:
```bash
streamlit run app.py
```

## Usage Guide

### 1. API Key Configuration

1. Visit [OpenAI Platform](https://platform.openai.com/account/api-keys) to obtain your API key
2. Launch the application and locate the API key input section
3. Enter your OpenAI API key in the secure input field
4. Click "Submit" to save your configuration

### 2. Document Upload

1. Navigate to the upload section
2. Click "Browse Files" to select your PDF document(s)
3. Wait for the upload and indexing process to complete
4. The system will confirm when your document is ready for querying

### 3. Asking Questions

1. Type your question in the chat input box
2. Click "Send" or press Enter to submit
3. The AI will process your question and provide a context-aware response
4. Continue the conversation naturally with follow-up questions

### 4. Advanced Configuration

- Model Selection: Choose between GPT-3.5-Turbo and GPT-4
- Temperature Setting: Adjust from 0.1 (focused) to 1.0 (creative)
- Context Window: Customize the amount of conversation history maintained

## Architecture

The application is built on a modern stack:

- Frontend: Streamlit framework
- Document Processing: LlamaIndex
- Language Model: OpenAI GPT
- Vector Storage: LlamaIndex VectorStoreIndex
- Session Management: Streamlit state management

## Development

### Setup Development Environment

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Unix
venv\Scripts\activate     # Windows
```

2. Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Troubleshooting

Common issues and solutions:

- **API Key Issues**: Ensure your OpenAI API key is valid and has sufficient credits
- **PDF Loading Errors**: Check if your PDF is text-based and not scanned
- **Memory Issues**: Try processing smaller documents or adjusting chunk sizes
- **Response Quality**: Adjust the temperature parameter for different response styles

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact & Support

- Author: [@holy_kau](https://twitter.com/holy_kau)
- Issues: Please use the GitHub issues tab
- Discussions: Join our [Discord community](#)

## Acknowledgments

- OpenAI for their powerful language models
- Streamlit team for the excellent framework
- LlamaIndex for document processing capabilities
- All contributors and users of this project

---

Made with ❤️ by Kaushal | [Support my work](https://www.buymeacoffee.com/kaushal.ai)