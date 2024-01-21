from fastapi import FastAPI, Depends, HTTPException
from typing import Annotated
from app.database.schemas.ticketDB import Ticket
from app.database.schemas.trainDB import Train
from app.database.database import engine, SessionLocal
from sqlalchemy.orm import Session
from app.database import database as database
import smtplib
from email.mime.text import MIMEText

app = FastAPI()
database.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/alive", status_code=status.HTTP_200_OK)
async def ticket_alive():
    return {'message' : 'service alive'}

@app.get("/ticket/{ticket_id}")
async def fetch_tickets(ticket_id: int, db: db_dependency):
    try:
        result = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    except Exception:
        raise HTTPException(status_code=404, detail='Tickets not found')
    return result


def check_train_existence(direction: str, db: db_dependency):
    return db.query(Train).filter(
        Train.direction == direction
    ).first()


def send_email(message: str, sender: str, receiver: str):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    server.login(sender, "bxmq ndfl fmcv ybzhpip")
    msg = MIMEText(message)
    msg['Subject'] = "Click me please"
    server.sendmail(sender, receiver, msg.as_string())

    return "Success"



@app.post("/buy_ticket")
async def buy_ticket(direction: str,
                     name: str,
                     second_name: str,
                     email: str,
                     db: db_dependency):
    try:
        train = check_train_existence(direction, db)
        if train.remaining_seats > 0:
            ticket = Ticket(user_name=name,
                            user_second_name=second_name,
                            user_email=email,
                            train_id=train.id,
                            departure_date=train.departure_date)
            send_email(f"{ticket.user_name} {ticket.user_second_name}, your train departs on {ticket.departure_date}",
                       "antonshepitko99@gmail.com",
                       ticket.user_email)
            train.remaining_seats -= 1
            db.add(ticket)
            db.commit()
            db.refresh(ticket)
    except HTTPException as e:
        print(f"Error: {e}")

