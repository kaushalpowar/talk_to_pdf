# Talk to PDF 🤖 📑️

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.38.0-FF4B4B.svg)](https://streamlit.io)
[![OpenAI](https://img.shields.io/badge/OpenAI-1.43.0-412991.svg)](https://openai.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

Talk to PDF is an innovative web application that enables natural language interaction with PDF documents through an AI-powered interface. Using state-of-the-art language models from OpenAI and the Streamlit framework, users can ask questions about PDF content and receive instant, context-aware responses.

### Key Features

- 📚 Natural language interaction with PDF documents
- 🔍 Advanced document processing and indexing
- 💬 Context-aware question answering
- ⚡ Real-time response streaming
- 🎛️ Customizable AI model parameters
- 📱 User-friendly web interface

## Requirements

- Python 3.11 or higher
- OpenAI API key
- Modern web browser
- Internet connection

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

### 1. API Key Configuration

- Launch the application
- Navigate to the "Enter your OpenAI API key" section
- Obtain an API key from [OpenAI Platform](https://platform.openai.com/account/api-keys)
- Enter your API key in the secure input field
- Click "Submit" to save the configuration

### 2. Document Upload

- Go to the "Upload PDF" section
- Click "Browse Files" to select your PDF
- Support for multiple PDF files
- Wait for the indexing process to complete

### 3. Interactive Chat

- Type your questions in the chat input box
- Get AI-powered responses based on document content
- Maintain context throughout the conversation
- Adjust model parameters for different response styles

### 4. Advanced Settings

- Choose between different OpenAI models (GPT-3.5-turbo or GPT-4)
- Adjust temperature settings (0.1-1.0) for response creativity
- Customize other parameters as needed

## Technical Architecture

The application is built on three main components:

1. **Frontend Interface**: Streamlit-based web application
2. **Document Processing**: LlamaIndex for PDF parsing and indexing
3. **AI Integration**: OpenAI's language models for understanding and response generation

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Support

For support and questions, please reach out to:
- Twitter: [@holy_kau](https://twitter.com/holy_kau)
- GitHub Issues: [Create an issue](https://github.com/yourusername/talk-to-pdf/issues)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- OpenAI for providing the language models
- Streamlit team for the amazing framework
- LlamaIndex for document processing capabilities

---

Made with ❤️ by [Kaushal](https://twitter.com/holy_kau)

Enjoy interacting with your PDFs using natural language! 🚀📄