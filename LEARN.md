# Talk to PDF 🤖 📑️

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.38.0-FF4B4B.svg)](https://streamlit.io)
[![OpenAI](https://img.shields.io/badge/OpenAI-1.43.0-412991.svg)](https://openai.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An intelligent document interaction system that enables natural language conversations with PDF documents using state-of-the-art AI technology. Ask questions about your PDFs and receive instant, context-aware responses powered by OpenAI's language models.

## 🚀 Features

- Natural language interaction with PDF documents
- Context-aware question answering
- Real-time response streaming
- Support for multiple PDF files
- Customizable AI model parameters
- User-friendly chat interface
- Secure API key management

## 📋 Requirements

- Python 3.11 or higher
- OpenAI API key
- Streamlit 1.38.0
- LlamaIndex 0.11.3
- Other dependencies listed in `requirements.txt`

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/talk-to-pdf.git
cd talk-to-pdf
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## 🎯 Usage

### 1. API Key Configuration

- Launch the application and navigate to the API key section
- Obtain an OpenAI API key from [OpenAI Platform](https://platform.openai.com/account/api-keys)
- Enter your API key in the secure input field
- Click "Submit" to save your configuration

### 2. Document Upload

- Navigate to the upload section
- Click "Browse Files" to select your PDF(s)
- Support for single or multiple PDF uploads
- Wait for document processing and indexing

### 3. Interactive Chat

- Use the chat interface to ask questions about your documents
- Type your question in the input box
- Click "Send" or press Enter to submit
- Receive AI-generated responses based on document content

### 4. Advanced Options

- Select between different OpenAI models (GPT-3.5-turbo or GPT-4)
- Adjust temperature settings for response creativity
- Configure other model parameters as needed

## ⚙️ Configuration

The application supports various configuration options:

| Parameter    | Description                | Default Value |
|-------------|----------------------------|---------------|
| Model       | OpenAI model selection     | gpt-3.5-turbo |
| Temperature | Response randomness (0-1)  | 0.5          |
| Chunk Size  | Document processing size   | 1000         |

## 🔍 Troubleshooting

Common issues and solutions:

1. **API Key Issues**
   - Verify API key is correct
   - Check OpenAI account status
   - Ensure sufficient API credits

2. **PDF Processing Errors**
   - Confirm PDF is not corrupted
   - Check file size limits
   - Ensure PDF is text-based (not scanned)

3. **Performance Issues**
   - Reduce document size if necessary
   - Check internet connection
   - Clear browser cache

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📬 Contact

Created by [Kaushal](https://twitter.com/holy_kau)

For questions and feedback:
- Twitter: [@holy_kau](https://twitter.com/holy_kau)
- GitHub Issues: [Project Issues](https://github.com/yourusername/talk-to-pdf/issues)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Enjoy interacting with your PDFs using natural language! 🚀📄