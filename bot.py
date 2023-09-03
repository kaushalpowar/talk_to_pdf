import streamlit as st
from streamlit.components.v1 import html
from langchain.document_loaders import PyPDFLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
import os
import tempfile
import pysqlite3
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')


st.set_page_config(page_title="Talk to PDF", page_icon=":robot_face:", layout="wide")
st.title("Talk to your PDF 🤖 📑️")
def main():
    html_temp = """
                       <div style="background-color:{};padding:1px">

                       </div>
                       """


    button = """
<script type="text/javascript" src="https://cdnjs.buymeacoffee.com/1.0.0/button.prod.min.js" data-name="bmc-button" data-slug="kaushal.ai" data-color="#FFDD00" data-emoji=""  data-font="Cookie" data-text="Support my work" data-outline-color="#000000" data-font-color="#000000" data-coffee-color="#ffffff" ></script>"""
    with st.sidebar:
        st.markdown("""
        # ● About 
        "Talk to PDF" is an app that allows users to ask questions about the content of a PDF file using natural language. 
        
        The app uses a question-answering system powered by GPT 🔥 to provide accurate and relevant answers to the user's queries.       """)

        st.markdown(html_temp.format("rgba(55, 53, 47, 0.16)"), unsafe_allow_html=True)
        st.markdown("""
        # ● How does it work
        ・Upload a PDF file and ask questions about its content
        
        ・Get instant answers to your questions
        
        ・Powered by cutting-edge AI technology technology
        """)
        st.markdown(html_temp.format("rgba(55, 53, 47, 0.16)"), unsafe_allow_html=True)


        st.markdown("""
        Made by [@Obelisk_1531](https://twitter.com/Obelisk_1531)
        """)
        html(button, height=70, width=220)
        st.markdown(
            """
            <style>
                iframe[width="210"] {
                    position: fixed;
                    bottom: 60px;
                    right: 40px;
                }
            </style>
            """,
            unsafe_allow_html=True,
        )

    # Get OpenAI API key from user
    st.subheader("Step 1: Enter your OpenAI API key")
    api_key = st.text_input("Enter your OpenAI API key. (https://platform.openai.com/account/api-keys)", type="password")
    submit = st.button("Submit")

    if submit:
         # Set OpenAI API key
        os.environ["OPENAI_API_KEY"] = api_key


    st.subheader("Step 2: Upload your PDF")
    pdf_file = st.file_uploader(
        "Unleash the power of AI to have a conversation with your PDFs and uncover new insights, all with a single upload⬇️ ",
        type='pdf', accept_multiple_files=False)
    if pdf_file is not None:
        # Save uploaded file to temporary file
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(pdf_file.read())
            tmp_file.flush()

            # Load and split PDF pages
            loader = PyPDFLoader(tmp_file.name)

            # Create an index using the loaded documents
            index_creator = VectorstoreIndexCreator()
            docsearch = index_creator.from_loaders([loader])

            # Create a question-answering chain using the index
            chain = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff",
                                                retriever=docsearch.vectorstore.as_retriever(),
                                                input_key="question")

            # Add text input widget for user to enter query
            query = st.text_input("Ask a question")
            st.button("Ask")

            # Check if a query was entered
            if query:
                # Pass the query to the chain
                response = chain({"question": query})
                if response:
                    with st.spinner("PDF is about to talk..."):
                        # Display the response
                        st.write(response['result'])



if __name__ == "__main__":
    main()
