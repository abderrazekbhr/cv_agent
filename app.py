import logging

from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import Response
import  inngest.fast_api

from controllers.agent_about import router as about

from pydantic import BaseModel

# inngest_client=inngest.Inngest(
#     app_id="rag_app",
#     logging=logging.getLogger("uvicorn"),
#     is_production=False,
#     serializer=inngest.PydanticSerializer()
    
# )



app=FastAPI(
    title="agent webapp",   
    debug=False,
    description="this app is used to let your app access to the agents "    
)

# inngest.fast_api.serve(
#     app,inngest_client
# )

app.include_router(
    prefix="/about",
    router=about
)

     