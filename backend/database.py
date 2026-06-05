# database.py
# Sets up the database connection.
# SQLAlchemy is like a translator between Python and PostgreSQL.

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings

# Create the database engine
engine = create_engine(
    settings.database_url,
    # These settings improve performance
    pool_pre_ping=True,     # Check connection is alive before using it
    pool_recycle=300,       # Refresh connections every 5 minutes
    echo=True if settings.environment == "development" else False
)

# SessionLocal is a factory that creates database sessions
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base is the parent class all our database models will inherit from
Base = declarative_base()

# This function gives us a database session for each API request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()