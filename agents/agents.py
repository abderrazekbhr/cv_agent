import os
from typing import Optional
from typing_extensions import Literal

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

class AgentResponse(BaseModel):
    kind: Literal["data", "issue"]
    data: Optional[ResponseData] = None
    issue: Optional[ResponseIssue] = None


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


 
def load_system_prompt(file_name: str) -> str:
    with open(f"agents/prompts/{file_name}", "r") as file:
        prompt = file.read()
    return prompt


agent_initializer = GeminiAgent()


search_agent = agent_initializer.create_agent(
    system_prompt=load_system_prompt("search_prompt.txt"),
    response_format=None,
    tools=[]
)

cv_agent = agent_initializer.create_agent(
    tools=[get_information_rag],
    system_prompt=load_system_prompt("cv_prompt.txt"),
    response_format=AgentResponse
)



# qa_agent = agent_initializer.create_agent(
#     tools=[get_information_rag],
#     system_prompt=load_system_prompt("qa_prompt.txt"),
# )








