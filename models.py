import datetime

from sqlalchemy import Column, Float, Integer, String, DateTime
from sqlalchemy.orm import declarative_base


Base = declarative_base()

class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    price = Column(Float)
    date_added = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
