from database.session import Base
from sqlalchemy import Column, Integer, String

class Configuration(Base):
    __tablename__ = 'configurations'

    id = Column(Integer, primary_key=True)
    download_dir = Column(String, nullable=False)
    msu_master_dir = Column(String, nullable=False)
    tracker_path = Column(String, nullable=True)
    dark_mode = Column(Integer, default=0)
    auto_run = Column(Integer, default=0)
    sfc_file = Column(String, nullable=True)