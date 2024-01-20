from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import List, Annotated
from database.schemas import trainDB as models
from database.database import engine, SessionLocal
from sqlalchemy.orm import Session
from model.train import Train

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/trains")
async def fetch_trains(db: db_dependency):
    result = db.query(models.Train).all()
    return result


@app.post("/add_train")
async def add_trains(train: Train, db: db_dependency):
    db_train = models.Train(model=train.model,
                            departure_date=train.departure_date,
                            remaining_seats=train.remaining_seats)
    db.add(db_train)
    db.commit()
    db.refresh(db_train)
