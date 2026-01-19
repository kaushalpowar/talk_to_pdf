# Talk to PDF 🤖 📑️

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.38.0-red.svg)](https://streamlit.io/)
[![OpenAI](https://img.shields.io/badge/OpenAI-API-green.svg)](https://openai.com/)

An intelligent document interaction system that enables natural language conversations with PDF documents. Powered by OpenAI's language models and Streamlit, this application allows users to extract insights and information from PDFs through simple questions and answers.

## 🌟 Features

- Natural language interaction with PDF documents
- Real-time AI-powered responses
- Context-aware conversation handling
- Support for multiple PDF formats
- Secure API key management
- Interactive chat interface
- Streaming responses for better user experience

## 📋 Requirements

- Python 3.11 or higher
- OpenAI API key
- Internet connection
- Modern web browser

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

3. Launch the application:
```bash
streamlit run app.py
```

## 📖 Usage Guide

### 1. API Key Setup
- Visit [OpenAI Platform](https://platform.openai.com/account/api-keys) to obtain your API key
- Launch the application and locate the "Enter your OpenAI API key" section
- Enter your API key securely in the password-protected input field
- Click "Submit" to validate and store your key

### 2. Document Upload
- Navigate to the upload section
- Click "Browse Files" or drag and drop your PDF
- Support for multiple PDF files
- Wait for the processing indicator to complete

### 3. Asking Questions
- Type your question in the chat input box
- Questions can be about any content within the uploaded PDF
- Support for follow-up questions with context awareness
- Real-time response streaming

### 4. Managing Responses
- View responses in a conversational format
- Scroll through chat history
- Clear conversation if needed
- Export chat history (coming soon)

## 🔒 Security Considerations

- API keys are stored securely in session state
- Documents are processed locally
- No permanent storage of uploaded files
- Secure HTTPS communication

## 🛠 Technical Architecture

- Frontend: Streamlit framework
- Backend: Python with OpenAI integration
- Document Processing: LlamaIndex
- Vector Storage: Optimized for quick retrieval
- Chat Engine: Context-aware response generation

## 🔧 Troubleshooting

Common issues and solutions:

1. **API Key Issues**
   - Verify key is correctly copied from OpenAI dashboard
   - Check for leading/trailing whitespace
   - Ensure proper API access level

2. **PDF Processing**
   - Maximum file size: 100MB
   - Supported formats: Standard PDF
   - Text must be machine-readable

3. **Performance**
   - Large documents may require longer processing time
   - Consider splitting very large PDFs
   - Optimal performance with documents under 50 pages

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Author

Created by [Kaushal](https://twitter.com/holy_kau)

## 🙏 Acknowledgments

- OpenAI for their powerful language models
- Streamlit team for the amazing framework
- LlamaIndex for document processing capabilities
- All contributors and users of this project

---

Enjoy exploring your PDFs through natural conversation! 🚀📄

For issues, feature requests, or questions, please [open an issue](https://github.com/yourusername/talk-to-pdf/issues) or reach out on Twitter.