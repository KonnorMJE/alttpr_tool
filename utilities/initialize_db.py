import os
import logging

from config import BASE_DIR
from database.session import Base, engine
from database.models import Configuration
from database.session import Session


def initialize_db():
    """
    Initialize the database and create default configuration if necessary.

    This function sets up the database tables using SQLAlchemy and creates a default
    configuration record if one does not already exist.
    """
    logging.info("Initializing database")
    Base.metadata.create_all(engine)

    with Session() as session:
        if not session.query(Configuration).first():
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            default_download_dir = os.path.join(base_dir, '_internal', 'CHANGEME')
            default_msu_master_dir = os.path.join(base_dir, '_internal', 'CHANGEME')
            
            # Create directories
            os.makedirs(default_download_dir, exist_ok=True)
            os.makedirs(default_msu_master_dir, exist_ok=True)
            
            default_config = Configuration(
                download_dir=default_download_dir,
                msu_master_dir=default_msu_master_dir,
                dark_mode=0,
                auto_run=0
            )
            session.add(default_config)
            session.commit()
            logging.info("Default configuration added to database")
