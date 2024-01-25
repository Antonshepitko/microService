    import os

    import uvicorn
    from fastapi import FastAPI, Depends, HTTPException, status
    from pydantic import BaseModel
    from typing import List, Annotated
    from sqlalchemy.orm import Session
    from model.train import Train as TrainModel
    from datetime import datetime
    from uuid import UUID

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


@app.get("/get_train_by_id/{train_id}")
async def get_train_by_id(train_id: UUID):
    for train in db:
        if train.id == train_id:
            return train
    raise HTTPException(
        status_code=404,
        detail=f'train with {train_id} does not exist'
    )


@app.delete("/delele_train/{train_id}")
async def delete_train(train_id: UUID):
    for train in db:
        if train.id == train_id:
            db.remove(train)
            return
    raise HTTPException(
        status_code=404,
        detail=f'train with {train_id} does not exist'
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('PORT', 80)))
