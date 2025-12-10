import os

from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI

from agents.tools.tools import  get_information_rag
from pydantic import BaseModel,Field


class ResponseData(BaseModel):
    information:str
    
class ResponseIssue(BaseModel):
    tile:str
    descritpion:str


# --- 2. SETUP ---
SYSTEM_PROMPT = """You are an expert chasseur de tete  who speaks in puns.

You have access to two tools:

- get_information_rag: is a methode that give related data to cv  

if a user ask you about something off me use the tools and reformulate the ressource to generate response to the query and if related data doesn't response to the query return ResponseIssue.
"""


model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0,
    max_tokens=1000
 
)


cv_agent = create_agent(
    model=model,
    tools=[get_information_rag],
    system_prompt=SYSTEM_PROMPT,
    response_format=ResponseData|ResponseIssue
)









