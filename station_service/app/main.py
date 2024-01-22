import os

import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Annotated
from app.database.schemas.trainDB import Train
from app.database.database import engine, SessionLocal
from sqlalchemy.orm import Session
from app.model.train import Train as TrainModel
import app.database.database as database

app = FastAPI()
database.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/health", status_code=status.HTTP_200_OK)
async def station_alive():
    return {'message': 'service alive'}


@app.get("/trains")
async def fetch_trains(db: db_dependency):
    result = db.query(Train).all()
    return result


@app.post("/add_train")
async def add_trains(train: TrainModel, db: db_dependency):
    db_train = Train(model=train.model,
                     direction=train.direction,
                     departure_date=train.departure_date,
                     remaining_seats=train.remaining_seats)
    db.add(db_train)
    db.commit()
    db.refresh(db_train)


@app.post("/delete_train")
async def delete_train(train_id: int, db: db_dependency):
    try:
        train = db.query(Train).filter(
            Train.id == train_id,
        ).first()
        db.delete(train)
        db.commit()
    except Exception as _ex:
        raise HTTPException(status_code=404, detail='Train not found')


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('PORT', 80)))
