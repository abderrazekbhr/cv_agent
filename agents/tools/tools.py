from langchain.tools import tool
import requests as rq
from agents.pipeline.ingest_cv import rag_ingest_pipeline



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


@tool
def fetch_post_content(url: str) -> str:
    """Fetches the content of a blog post from the given URL."""
    response = rq.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return f"Failed to fetch content. Status code: {response.status_code}"
    
