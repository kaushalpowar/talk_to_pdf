# Talk to PDF 🤖 📑️

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.38.0-FF4B4B.svg)](https://streamlit.io)
[![OpenAI](https://img.shields.io/badge/OpenAI-1.43.0-412991.svg)](https://openai.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An intelligent document interaction system that enables natural language conversations with PDF documents using state-of-the-art AI technology.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Requirements](#requirements)
- [Usage Guide](#usage-guide)
- [Technical Architecture](#technical-architecture)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Features
- 🔍 Natural language querying of PDF documents
- 🤖 Powered by OpenAI's advanced language models
- 💬 Interactive chat interface for document exploration
- 📊 Context-aware responses with high accuracy
- ⚡ Real-time streaming responses
- 🎛️ Customizable model parameters

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/talk-to-pdf.git

# Navigate to project directory
cd talk-to-pdf

# Install required packages
pip install -r requirements.txt
```

## Requirements
- Python 3.11 or higher
- OpenAI API key
- Streamlit 1.38.0
- LlamaIndex 0.11.3
- Other dependencies listed in requirements.txt

## Usage Guide

### 1. API Key Configuration
1. Visit [OpenAI Platform](https://platform.openai.com/account/api-keys) to obtain your API key
2. Launch the application and locate the "Enter your OpenAI API key" section
3. Input your API key in the secure password field
4. Click "Submit" to authenticate

### 2. Document Upload
1. Navigate to the upload section
2. Click "Browse Files" to select your PDF document
3. Support for multiple PDF files available
4. Wait for the processing indicator to complete

### 3. Interactive Querying
1. Use the chat interface to ask questions about your document
2. Type your query in natural language
3. Receive AI-powered responses based on document content
4. Continue the conversation with follow-up questions

### 4. Advanced Options
- Select between different GPT models (gpt-3.5-turbo or gpt-4)
- Adjust temperature settings for response creativity
- Customize other parameters as needed

## Technical Architecture

The application is built on three main components:
1. **Frontend Interface**: Streamlit-based web application
2. **Document Processing**: LlamaIndex for document indexing and retrieval
3. **AI Integration**: OpenAI's language models for natural language understanding

## Configuration

```python
# Example configuration options
config = {
    "model_options": ["gpt-3.5-turbo", "gpt-4"],
    "temperature_range": (0.1, 1.0),
    "default_temperature": 0.5,
    "chunk_size": 1000,
    "max_tokens": 4096
}
```

## Troubleshooting

Common issues and solutions:
- **API Key Error**: Ensure your OpenAI API key is valid and has sufficient credits
- **PDF Loading Failed**: Check if the PDF is corrupted or password-protected
- **Slow Response**: Consider reducing document size or adjusting chunk parameters

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Created by [Kaushal](https://twitter.com/holy_kau)

---

Enjoy exploring your PDFs through natural conversation! 🚀📄

For questions, feedback, or support:
- 📧 Email: [contact@example.com](mailto:contact@example.com)
- 🐦 Twitter: [@holy_kau](https://twitter.com/holy_kau)
- 💬 GitHub Issues: [Report a bug](https://github.com/yourusername/talk-to-pdf/issues)