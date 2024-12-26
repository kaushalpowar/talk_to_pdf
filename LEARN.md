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
- 🔒 Secure API key management

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

## Requirements

- Python 3.11 or higher
- OpenAI API key
- Streamlit 1.38.0
- Other dependencies listed in `requirements.txt`

## Usage Guide

### 1. API Key Setup

1. Obtain an OpenAI API key from [OpenAI Platform](https://platform.openai.com/account/api-keys)
2. Launch the application and navigate to the API key section
3. Enter your API key in the secure input field
4. Click "Submit" to save the key

> ⚠️ **Security Note**: Your API key is stored securely in the session state and is never exposed or stored permanently.

### 2. Document Upload

1. Navigate to the upload section
2. Click "Browse Files" to select your PDF document(s)
3. Wait for the upload and indexing process to complete
4. The system will confirm when your document is ready for querying

### 3. Asking Questions

1. Type your question in the input box
2. Click "Ask" or press Enter to submit
3. View the AI-generated response in real-time
4. Continue the conversation naturally with follow-up questions

### 4. Advanced Options

- Select between different OpenAI models (GPT-3.5-turbo or GPT-4)
- Adjust temperature settings for response creativity
- Configure context window size for better accuracy

## Architecture

The application follows a three-tier architecture:
1. **Frontend**: Streamlit-based user interface
2. **Processing Layer**: Document indexing and query processing
3. **AI Layer**: OpenAI integration for natural language understanding

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

### Running Locally

```bash
streamlit run 0_🔌API_KEY.py
```

## Troubleshooting

Common issues and solutions:

- **API Key Issues**: Ensure your OpenAI API key is valid and has sufficient credits
- **PDF Loading Errors**: Check if your PDF is text-based and not scanned
- **Memory Issues**: Try splitting large PDFs into smaller documents

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

Author: [Kaushal](https://twitter.com/holy_kau)

Project Link: [https://github.com/yourusername/talk-to-pdf](https://github.com/yourusername/talk-to-pdf)

---

Made with ❤️ by Kaushal | [Support my work](https://www.buymeacoffee.com/kaushal.ai)