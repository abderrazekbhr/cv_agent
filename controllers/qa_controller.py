from fastapi import APIRouter, Body, HTTPException,Response
from fastapi.params import Query
from agents.agents import  search_agent


router=APIRouter()
@router.post("/search")
def search_web(query: str = Body(..., embed=True)):
    messages={"messages":[{
        "role":"user",
        "content": f"Perform a web search and provide the most relevant information about this: {query}"
    }]}

    response = search_agent.invoke(messages)


    return response 