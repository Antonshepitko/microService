from pydantic import BaseModel, ConfigDict
from datetime import datetime


class Train(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    model: str
    direction: str
    departure_date: datetime
    remaining_seats: int
