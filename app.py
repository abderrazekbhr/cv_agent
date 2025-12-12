
from fastapi import FastAPI
from config.db import Base,engine
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from controllers.users import router as user_router

load_dotenv()

from controllers.agent_about import router as about
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    print("Starting up...")

    Base.metadata.create_all(bind=engine)
    yield

    # Shutdown code
    print("Shutting down...")


app=FastAPI(
    title="Agent Web App",   
    debug=False,
    description="this app is used to let your app access to the agents "    ,
    lifespan=lifespan
)

app.include_router(
    tags=["User Management"],
    prefix="/user",
    router=user_router
)

app.include_router(
    tags=["About"],
    prefix="/about",
    router=about
)


