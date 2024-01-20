from sqlalchemy import Column, String, DateTime, Integer
from ..database import Base


class Train(Base):
    __tablename__ = 'trains'

    id = Column(Integer, primary_key=True, index=True)
    model = Column(String, nullable=False)
    direction = Column(String, nullable=False)
    departure_date = Column(DateTime, nullable=False)
    remaining_seats = Column(Integer, nullable=False)
