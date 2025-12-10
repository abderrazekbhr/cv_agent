from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import os 


# --- DATABASE CONFIGURATION ---
DATABASE_URL = f"postgresql+psycopg://{os.getenv('USERNAME_DB')}:{os.getenv('PASSWORD_DB')}@localhost:5432/{os.getenv('DB_NAME')}"


engine = create_engine(
    DATABASE_URL,
    echo=True,           # log SQL queries for debugging
    pool_size=10,        # number of connections in the pool
    max_overflow=20      # number of connections that can be created after the pool reached its size
)

def get_db():
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


Base = declarative_base()

