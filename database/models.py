from sqlalchemy import Column, Integer, String, Boolean

from alttpr_tool.database.session import Base

class Configuration(Base):
    __tablename__ = 'configurations'

    id = Column(Integer, primary_key=True)
    download_dir = Column(String)
    msu_master_dir = Column(String)
    tracker_path = Column(String, nullable=True)
    dark_mode = Column(Boolean, default=False)
    auto_run = Column(Boolean, default=False)
    sfc_file = Column(String, nullable=True)