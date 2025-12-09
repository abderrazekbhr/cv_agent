
from fastapi import FastAPI
from config.db import Base,engine
from controllers.agent_about import router as about

from contextlib import asynccontextmanager

@asynccontextmanager
def lifespan(app: FastAPI):
    # Startup code
    print("Starting up...")
    Base.metadata.create_all(bind=engine)
    
    yield
    # Shutdown code
    print("Shutting down...")



app=FastAPI(
    title="agent webapp",   
    debug=False,
    description="this app is used to let your app access to the agents "    ,
    lifespan=[lifespan]
)


app.include_router(
    prefix="/about",
    router=about
)


