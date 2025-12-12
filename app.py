
from fastapi import FastAPI
from config.db import Base,engine
from dotenv import load_dotenv
from contextlib import asynccontextmanager

from controllers.users_controller import router as user_router
from controllers.qa_controller import router as qa_router
from controllers.about_controller import router as about

load_dotenv()

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

app.include_router(
    tags=["QA"],
    prefix="/qa",
    router=qa_router
)
