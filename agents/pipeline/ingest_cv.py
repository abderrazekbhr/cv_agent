from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.documents import Document

from pypdf import PdfReader
import os

from config.bucket import bucket_client



def load_file(file_path:str):
    data=bucket_client().get_object(
        "s3-cv",
        file_path
    )
    with open("temp.pdf","wb") as f:
        f.write(data.read())
    loader=PdfReader("temp.pdf")
    
    text=loader.pages[0].extract_text() if len(loader.pages)>0 else None
    docs=[Document(page_content=text)]
    
    return docs

def rag_ingest_pipeline(file_path:str):
    """this function return related to query passed"""
    
    # Prepare Embbeddings
    embeddings=GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Prepare chroma db
    vector_store = Chroma(
        collection_name="example_collection",
        embedding_function=embeddings,
        persist_directory="./chroma_langchain_db",  # Where to save data locally, remove if not necessary
    )
    
    # Check if file already exists
    existing = vector_store.get(where={"source": file_path})
    if existing and existing['ids']:
        return vector_store
    
    # Loading file
    docs = load_file(file_path=file_path)
    
    # Splitting text
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, chunk_overlap=100, add_start_index=True
    )
    
    all_splits = text_splitter.split_documents(docs)

    # Add source metadata to each chunk
    for doc in all_splits:
        doc.metadata["source"] = file_path
    
    #Embedding text as vector
    vector_store.add_documents(documents=all_splits)

    return vector_store

