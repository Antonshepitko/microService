import os

import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List, Annotated
from app.database.database import engine, SessionLocal
from sqlalchemy.orm import Session
from app.model.train import Train as TrainModel
from datetime import datetime

app = FastAPI()

db: List[TrainModel] = [
    TrainModel(
        id=UUID('86f053a0-0dd1-4439-ba43-bdf586220bd2'),
        model='Test',
        direction="St. Petersburg",
        departure_date=datetime(2022, 5, 15, 12, 30, 0),
        remaining_seats=10
    )
]

db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/health", status_code=status.HTTP_200_OK)
async def station_alive():
    return {'message': 'service alive'}


@app.get("/trains")
async def fetch_trains():
    return db


@app.post("/add_train")
async def add_trains(train: TrainModel):
    db.append(train)
    return {"id": train.id}


@app.delete("/trains/{train_id}")
async def delete_user(train_id: UUID):
    for train in db:
        if train.id == train_id:
            db.remove(train)
            return
    raise HTTPException(
        status_code=404,
        detail=f'train with {train_id} does not exist'
    )
