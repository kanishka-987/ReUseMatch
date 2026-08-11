import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_USER = os.getenv("DB_USER", "reuse_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "placeholder_password")
DB_NAME = os.getenv("DB_NAME", "reuse_match")

# MySQL database URL
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create SQLAlchemy engine.
# Note: For SQLite, connect_args={"check_same_thread": False} would be needed, but MySQL is configured.
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """
    Dependency generator for FastAPI endpoints to yield database session instances.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
