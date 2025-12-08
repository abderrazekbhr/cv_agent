from langchain.tools import tool
import requests as rq
from agents.pipeline.ingest_cv import rag_ingest_pipeline
from dotenv import load_dotenv
import os
load_dotenv()



@tool
def get_information_rag(query:str,filename:str="cv.pdf")->list:
    
    """this function extract related information to query from cv passed in filename"""
    vector_store=rag_ingest_pipeline(file_path=filename)
    documents=vector_store.similarity_search(
        query=query,k=2
    )
    content=[]
    
    for doc in documents:
        content.append(doc.page_content)
    return content