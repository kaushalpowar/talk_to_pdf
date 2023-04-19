import streamlit as st
st.title('HI')
import os
os.environ["OPENAI_API_KEY"] = "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"
from langchain.document_loaders import UnstructuredPDFLoader
from langchain.indexes import VectorstoreIndexCreator
st.title("hi")
pdf_folder_path="Mitch Horowitz, Neville Goddard - Infinite Potential_ The Greatest Works of Neville Goddard (22 Oct 2019, St. Martin's Publishing Group_St. Martin’s Essentials) - libgen.li.pdf"
# location of the pdf file/files.
loaders = [UnstructuredPDFLoader(os.path.join(pdf_folder_path, fn)for fn in os.listdir(pdf_folder_path))]

index = VectorstoreIndexCreator().from_loaders(loaders)


index.query('What is god?')
