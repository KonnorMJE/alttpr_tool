import os
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from pathlib import Path

from alttpr_tool.config import Config

# Create Base outside the class
Base = declarative_base()

class DatabaseSession:
    """Handles database session management"""
    _instance = None
    
    def __new__(cls):
        """Ensure only one instance exists (Singleton pattern)."""
        if cls._instance is None:
            cls._instance = super(DatabaseSession, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize database connection and session factory."""
        if not hasattr(self, 'initialized'):
            self.config = Config()
            self.database_path = self.config.DATABASE_DIR / 'alttpr_tool.db'
            
            # Ensure database directory exists
            self.database_path.parent.mkdir(parents=True, exist_ok=True)
            
            self.engine = create_engine(f'sqlite:///{self.database_path}')
            self.Session = sessionmaker(bind=self.engine)
            self.initialized = True
    
    @contextmanager
    def managed_session(self):
        """
        Context manager for database sessions.
        
        Yields:
            SQLAlchemy session object
        """
        session = self.Session()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
    
    def create_all(self):
        """Create all database tables."""
        Base.metadata.create_all(self.engine)
    
    def drop_all(self):
        """Drop all database tables."""
        Base.metadata.drop_all(self.engine)

# Create a singleton instance
db = DatabaseSession()
managed_session = db.managed_session

# Initialize tables
db.create_all()

