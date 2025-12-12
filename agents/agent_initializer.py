import os

from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI

from agents.tools.tools import  get_information_rag
from langchain.tools import BaseTool

from pydantic import BaseModel,Field


class ResponseData(BaseModel):
    information:str
    
class ResponseIssue(BaseModel):
    tile:str
    descritpion:str


class GeminiAgent:
    def __init__(self):    
        self.model = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0,
            max_tokens=1000 
        )

    def create_agent(self,tools:list[BaseTool],system_prompt:str,response_format:type):
        agent = create_agent(
            model=self.model,
            tools=tools,
            system_prompt=system_prompt,
            response_format=response_format
        )
        return agent



SYSTEM_PROMPT = """You are an expert in it and manager role need your help to responde to this question.

You have access to two tools:

- get_information_rag: is a methode that give related data to cv  
- fetch_post_content: is a methode that fetch content from url

if a user ask you about something off me use the tools and reformulate the ressource to generate response to the query and if related data doesn't response to the query return ResponseIssue.
"""



agent_initializer = GeminiAgent()

cv_agent = agent_initializer.create_agent(
    tools=[get_information_rag],
    system_prompt=SYSTEM_PROMPT,
    response_format=ResponseData|ResponseIssue
)

# qa_agent = agent_initializer.create_agent(
#     tools=[get_information_rag],
#     system_prompt=SYSTEM_PROMPT,
# )








