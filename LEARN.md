# Talk to PDF 🤖 📑️

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.38.0-FF4B4B.svg)](https://streamlit.io)
[![OpenAI](https://img.shields.io/badge/OpenAI-1.43.0-412991.svg)](https://openai.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An intelligent document interaction system that enables natural language conversations with PDF documents. Powered by OpenAI's language models and built with Streamlit, this application allows users to extract information and insights from PDFs through simple questions and answers.

## Features

- 📚 Natural language interaction with PDF documents
- 🔍 Context-aware question answering
- 🚀 Real-time response streaming
- 🎯 Customizable AI model parameters
- 🔒 Secure API key management
- 📱 Responsive web interface

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/talk-to-pdf.git
cd talk-to-pdf

# Install dependencies
pip install -r requirements.txt
```

## Requirements

- Python 3.11 or higher
- OpenAI API key
- Dependencies listed in `requirements.txt`

## Usage Guide

### 1. API Key Configuration

- Launch the application
- Navigate to the API key configuration section
- Obtain an OpenAI API key from [OpenAI Platform](https://platform.openai.com/account/api-keys)
- Enter your API key in the secure input field
- Click "Submit" to save your configuration

### 2. Document Upload

- Go to the PDF upload section
- Click "Browse Files" to select your PDF
- Support for multiple PDF uploads
- Wait for document processing to complete

### 3. Interactive Chat

- Type your questions in the chat input box
- Get AI-powered responses based on document content
- Maintain context throughout the conversation
- Adjust model parameters for different response styles

### 4. Advanced Options

- Choose between different OpenAI models (GPT-3.5-Turbo or GPT-4)
- Adjust temperature settings for response creativity
- Configure chunk size for document processing
- Customize response formatting

## Configuration

The application supports various configuration options:

```python
# Model Configuration
model_name = "gpt-3.5-turbo"  # or "gpt-4"
temperature = 0.5  # Range: 0.1 - 1.0
```

## Architecture

- Built on Streamlit framework
- Uses LlamaIndex for document processing
- OpenAI API integration for natural language understanding
- Vector-based document indexing for efficient retrieval
- Stream-based response generation

## Contributing

Contributions are welcome! Please feel free to submit pull requests or create issues for bugs and feature requests.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Support

For support and questions, please reach out to:
- Author: [Kaushal](https://twitter.com/holy_kau)
- GitHub Issues: [Project Issues](https://github.com/yourusername/talk-to-pdf/issues)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- OpenAI for providing the language models
- Streamlit team for the excellent web framework
- LlamaIndex for document processing capabilities

---

Made with ❤️ by [Kaushal](https://twitter.com/holy_kau)

Enjoy interacting with your PDFs using natural language! 🚀📄