import os

from config import BASE_DIR

from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

database_path = os.path.join(BASE_DIR, 'database', 'alttpr_tool.db')
Base = declarative_base()
engine = create_engine(f'sqlite:///{database_path}')
Session = sessionmaker(bind=engine)

@contextmanager
def managed_session():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

