
from fastapi import FastAPI
from config.db import Base,engine
from controllers.agent_about import router as about
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from controllers.users import router as user_router

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    print("Starting up...")
    # test_db_connection(app)
    Base.metadata.create_all(bind=engine)
    
    yield
    # Shutdown code
    print("Shutting down...")


app=FastAPI(
    title="agent webapp",   
    debug=False,
    description="this app is used to let your app access to the agents "    ,
    lifespan=lifespan
)


app.include_router(
    prefix="/about",
    router=about
)
app.include_router(
    prefix="/user",
    router=user_router
)


