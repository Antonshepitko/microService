from pydantic import BaseModel, ConfigDict
from datetime import datetime
from uuid import UUID


class Train(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    model: str
    direction: str
    departure_date: datetime
    remaining_seats: int
