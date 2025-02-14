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
        settings_exists = session.query(Configuration).first() is not None

        if not settings_exists:
            change_me_dir = os.path.join(BASE_DIR, "CHANGEME")
            if not os.path.exists(change_me_dir):
                os.mkdir(change_me_dir)
                logging.info(f"Created 'CHANGEME' directory at {change_me_dir}")

            default_download_dir = change_me_dir
            default_msu_master_dir = change_me_dir
            default_config = Configuration(
                download_dir=default_download_dir,
                msu_master_dir=default_msu_master_dir,
                dark_mode=0,
                auto_run=0
            )
            session.add(default_config)
            session.commit()
            logging.info("Default configuration added to database")
