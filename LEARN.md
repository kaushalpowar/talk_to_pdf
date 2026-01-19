# Talk to PDF 🤖 📑️

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.38.0-FF4B4B.svg)](https://streamlit.io)
[![OpenAI](https://img.shields.io/badge/OpenAI-1.43.0-412991.svg)](https://openai.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An intelligent document interaction system that enables natural language conversations with PDF documents. Powered by OpenAI's language models and Streamlit, this application allows users to extract insights and information from PDFs through simple questions and answers.

## 🌟 Features

- Natural language interaction with PDF documents
- Powered by OpenAI's advanced language models
- Real-time streaming responses
- Context-aware conversation handling
- Support for multiple PDF documents
- User-friendly interface
- Customizable model parameters

## 📋 Requirements

- Python 3.11 or higher
- OpenAI API key
- Required Python packages (see `requirements.txt`)

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

3. Run the application:
```bash
streamlit run 0_🔌API_KEY.py
```

## 📖 Usage Guide

### 1. API Key Setup
- Launch the application
- Navigate to the API key configuration section
- Obtain an OpenAI API key from [OpenAI Platform](https://platform.openai.com/account/api-keys)
- Enter your API key in the secure input field
- Click "Submit" to save your configuration

### 2. Document Upload
- Go to the PDF upload section
- Click "Browse Files" or drag and drop your PDF
- Wait for the document processing to complete
- Multiple PDFs are supported

### 3. Interactive Chat
- Type your questions in the chat input
- Click "Send" or press Enter
- Receive AI-powered responses based on document content
- Maintain context-aware conversations

### 4. Customization Options
- Select between different OpenAI models (GPT-3.5-turbo or GPT-4)
- Adjust temperature settings for response variety
- Modify other parameters as needed

## ⚙️ Technical Details

- Built with Streamlit for the web interface
- Uses LlamaIndex for document processing and indexing
- Implements OpenAI's language models for comprehension
- Features real-time response streaming
- Maintains conversation context through session state

## 🔧 Troubleshooting

Common issues and solutions:

1. **API Key Issues**
   - Ensure your OpenAI API key is valid
   - Check for sufficient API credits
   - Verify network connectivity

2. **PDF Processing**
   - Ensure PDF is text-searchable
   - Check file size limits
   - Verify PDF is not password-protected

3. **Performance**
   - Large PDFs may take longer to process
   - Consider reducing document size if needed
   - Check system resources

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

Created by [Kaushal](https://twitter.com/holy_kau)

For questions, feedback, or support:
- Twitter: [@holy_kau](https://twitter.com/holy_kau)
- GitHub Issues: [Project Issues](https://github.com/yourusername/talk-to-pdf/issues)

---

Enjoy exploring your PDFs through natural conversation! 🚀📄