# Talk to PDF 🤖 📑️

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.38.0-FF4B4B.svg)](https://streamlit.io)
[![OpenAI](https://img.shields.io/badge/OpenAI-1.43.0-412991.svg)](https://openai.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An intelligent document interaction system that enables natural language conversations with PDF documents. Powered by OpenAI's language models and built with Streamlit, Talk to PDF transforms how users extract information from documents through intuitive question-answering.

## 🚀 Features

- Natural language interaction with PDF documents
- Context-aware responses using advanced AI models
- Real-time streaming responses
- Support for multiple PDF uploads
- Adjustable AI parameters for customized responses
- User-friendly chat interface
- Secure API key management

## 📋 Requirements

- Python 3.11+
- OpenAI API key
- Dependencies listed in `requirements.txt`

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

3. Run the application:
```bash
streamlit run 0_🔌API_KEY.py
```

## 🎯 Usage

### 1. API Key Configuration
- Launch the application
- Navigate to the API key configuration section
- Obtain an OpenAI API key from [OpenAI Platform](https://platform.openai.com/account/api-keys)
- Enter your API key in the secure input field
- Click "Submit" to proceed

### 2. Document Upload
- Use the file upload interface to select your PDF(s)
- Supported format: PDF
- Multiple file upload supported
- Wait for document processing to complete

### 3. Interactive Chat
- Type your questions in the chat input
- Questions can be about any content within the uploaded PDF(s)
- Receive AI-powered responses in real-time
- Maintain context throughout the conversation

### 4. Customization Options
- Select between different GPT models (GPT-3.5-Turbo or GPT-4)
- Adjust temperature settings for response variety
- Configure other parameters as needed

## 🔧 Technical Architecture

- Frontend: Streamlit framework
- Document Processing: LlamaIndex
- Language Model: OpenAI GPT
- Vector Storage: LlamaIndex VectorStoreIndex
- State Management: Streamlit session state

## 🤔 Troubleshooting

Common issues and solutions:

1. **API Key Issues**
   - Ensure your OpenAI API key is valid and has sufficient credits
   - Check for any special characters or spaces in the API key

2. **PDF Processing Errors**
   - Verify PDF file is not corrupted
   - Ensure PDF is text-based and not scanned images
   - Check file size limits

3. **Response Generation**
   - If responses are slow, try adjusting the model parameters
   - For context issues, start a new chat session

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Contact

Created by [@Obelisk_1531](https://twitter.com/Obelisk_1531)

For questions, feedback, or support, please reach out through:
- Twitter: [@Obelisk_1531](https://twitter.com/Obelisk_1531)
- GitHub Issues: [Project Issues](https://github.com/yourusername/talk-to-pdf/issues)

---

Enjoy interacting with your PDFs using natural language! 🚀📄