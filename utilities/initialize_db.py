import os
import logging
from pathlib import Path
from sqlalchemy import create_engine

from alttpr_tool.config import Config
from alttpr_tool.database.session import db, Base
from alttpr_tool.database.models import Configuration

class DatabaseInitializer:
    """Handles database initialization and default configuration setup."""
    
    def __init__(self):
        """Initialize DatabaseInitializer with database session."""
        self.config = Config()
        self.db = db
        self.engine = self.db.engine
        
    def initialize(self):
        """
        Initialize the database and create default configuration if necessary.

        Creates database tables using SQLAlchemy and sets up default
        configuration if one doesn't exist.
        
        Raises:
            SQLAlchemyError: If database operations fail
            OSError: If directory creation fails
        """
        try:
            logging.info("Initializing database")
            self._create_tables()
            self._create_default_config()
        except Exception as e:
            logging.error(f"Database initialization failed: {e}")
            raise

    def _create_tables(self):
        """Create all database tables defined in models."""
        Base.metadata.create_all(self.engine)
        logging.info("Database tables created")

    def _create_default_config(self):
        """Create default configuration if none exists."""
        with self.db.managed_session() as session:
            if not session.query(Configuration).first():
                default_dirs = self._create_default_directories()
                config = self._create_config_record(
                    download_dir=default_dirs['download'],
                    msu_master_dir=default_dirs['msu']
                )
                session.add(config)
                session.commit()
                logging.info("Default configuration added to database")

    def _create_default_directories(self) -> dict:
        """
        Create default directories for downloads and MSUs.
        
        Returns:
            dict: Paths to created directories
        """
        base_dir = Path(Config.BASE_DIR)
        internal_dir = base_dir / '_internal'
        
        dirs = {
            'download': internal_dir / 'CHANGEME',
            'msu': internal_dir / 'CHANGEME'
        }
        
        for dir_path in dirs.values():
            dir_path.mkdir(parents=True, exist_ok=True)
            logging.info(f"Created directory: {dir_path}")
            
        return dirs

    def _create_config_record(self, download_dir: Path, msu_master_dir: Path) -> Configuration:
        """
        Create a new Configuration record.
        
        Args:
            download_dir: Path to download directory
            msu_master_dir: Path to MSU master directory
            
        Returns:
            Configuration: New configuration record
        """
        return Configuration(
            download_dir=str(download_dir),
            msu_master_dir=str(msu_master_dir),
            dark_mode=0,
            auto_run=0
        )