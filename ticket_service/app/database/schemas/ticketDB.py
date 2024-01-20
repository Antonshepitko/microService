from sqlalchemy import Column, String, DateTime, Integer
from ..database import Base


class Ticket(Base):
    __tablename__ = 'tickets'

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, nullable=False)
    user_second_name = Column(String, nullable=False)
    user_email = Column(String, nullable=False)
    train_id = Column(Integer, nullable=False)
    departure_date = Column(DateTime, nullable=False)
