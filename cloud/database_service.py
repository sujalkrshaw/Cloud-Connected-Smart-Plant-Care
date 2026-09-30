"""Database boundary. The main FastAPI app uses SQLAlchemy so SQLite and PostgreSQL share one data model."""
from backend.app.database import engine, SessionLocal, Base

def initialize_database():
    Base.metadata.create_all(bind=engine)
    return SessionLocal
