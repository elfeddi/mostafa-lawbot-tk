import os
import re
import uuid
from sentence_transformers import SentenceTransformer
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_voyageai import VoyageAIEmbeddings
import chromadb

voyemb = VoyageAIEmbeddings(
    voyage_api_key="pa-KT8QqDg8iYbFJTOLt6q-HqQRBftEghWmf9rJw7PBDco", model="voyage-law-2"
)

def preprocess_text(text):
    pattern = re.compile(r"(Article \d+)")
    processed_text = pattern.sub(r"\n### \1 ###\n", text)
    return processed_text

def split_documents(data):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100, separators=["\n### ", "\n\n", "\n", " "])
    texts = text_splitter.split_documents(data)
    if not texts:
        raise ValueError("Document splitting resulted in no chunks.")
    return texts

def embed_document(file_path, username):
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    for document in documents:
        document.page_content = preprocess_text(document.page_content)
    
    texts = split_documents(documents)

    client = chromadb.PersistentClient(path="vectorstore")
    collection_name = username
    col = client.get_or_create_collection(collection_name)

    for chunk in texts:
        chunk_id = str(uuid.uuid4())
        chunk_content = chunk.page_content
        chunk_metadata = chunk.metadata
        chunk_embeddings = voyemb.embed_documents([chunk_content])
        col.add(ids=[chunk_id], documents=[chunk_content], metadatas=[chunk_metadata], embeddings=chunk_embeddings)
