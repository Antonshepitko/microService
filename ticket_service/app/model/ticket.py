from pydantic import BaseModel, ConfigDict
from datetime import datetime


class Ticket(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_name: str
    user_second_name: str
    user_email: str
    train_id: int
    departure_date: datetime
