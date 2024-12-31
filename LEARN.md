# Talk to PDF 🤖 📑️

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-311/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.38.0-FF4B4B.svg)](https://streamlit.io)
[![OpenAI](https://img.shields.io/badge/OpenAI-1.43.0-412991.svg)](https://openai.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An intelligent document interaction system that enables natural language conversations with PDF documents using state-of-the-art AI technology.

## 🌟 Features

- Natural language interaction with PDF documents
- Real-time response streaming
- Context-aware conversation handling
- Support for multiple PDF files
- Customizable AI model parameters
- User-friendly interface
- Secure API key management

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/talk-to-pdf.git
cd talk-to-pdf
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## 🔧 Requirements

- Python 3.11 or higher
- OpenAI API key
- Streamlit 1.38.0
- LlamaIndex 0.11.3
- Other dependencies listed in `requirements.txt`

## 📖 Usage

### 1. API Key Configuration

- Launch the application and navigate to the API key section
- Obtain an OpenAI API key from [OpenAI Platform](https://platform.openai.com/account/api-keys)
- Enter your API key in the secure input field
- Click "Submit" to save your configuration

### 2. Document Upload

- Navigate to the upload section
- Click "Browse Files" to select your PDF document(s)
- Support for multiple PDF files
- Wait for the indexing process to complete

### 3. Interactive Chat

- Use the chat interface to ask questions about your documents
- Type your question in the input box
- Click "Send" or press Enter to submit
- Receive AI-generated responses based on document content

### 4. Advanced Settings

- Choose between different OpenAI models (GPT-3.5-turbo or GPT-4)
- Adjust temperature settings for response variation
- Customize other parameters as needed

## 🏗️ Architecture

The application is built on three main components:

1. **Frontend Interface**: Streamlit-based web application
2. **Document Processing**: LlamaIndex-powered document indexing and retrieval
3. **AI Integration**: OpenAI's language models for natural language understanding

## 🔒 Security

- API keys are securely handled and never stored permanently
- Document processing occurs locally
- Temporary files are automatically cleaned up
- No data is retained between sessions

## 🔍 Troubleshooting

Common issues and solutions:

1. **API Key Issues**
   - Verify your OpenAI API key is valid
   - Check for sufficient API credits
   - Ensure proper key input format

2. **PDF Processing Issues**
   - Ensure PDF is not password-protected
   - Check file size limits
   - Verify PDF is text-based (not scanned images)

3. **Response Issues**
   - Check internet connectivity
   - Verify model availability
   - Adjust temperature settings if responses are unclear

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Contact

Created by [@Obelisk_1531](https://twitter.com/Obelisk_1531)

For questions, feedback, or support:
- Twitter: [@Obelisk_1531](https://twitter.com/Obelisk_1531)
- GitHub Issues: [Project Issues](https://github.com/yourusername/talk-to-pdf/issues)

---

Enjoy interacting with your PDFs using natural language! 🚀📄