import pytest
import requests
from uuid import UUID, uuid4
from datetime import datetime
import json

station_url = 'https://localhost:8000'
ticket_url = 'https://localhost:8001'
add_train_url = f'{server_url}/add_train'
find_train_by_id_url = f'{station_url}/train_by_id/'

train_data = {
    "id": str(uuid4()),
    "model": "TrainModel123",
    "direction": "SomeDirection",
    "departure_date": str(datetime.now()),
    "remaining_seats": 50
}

ticket_data = {
    "direction": "Moscow",
    "name": "Anton",
    "second_name": "Shepitko",
    "email": "Moscow",
    "direction": "Moscow"
}


def test_train_get():
    pytest.assume(requests.post(add_train_url, json=train_data) == 200)
    res = requests.get(f"{find_train_by_id_url}/{train_data['id']}")
    pytest.assume('model' in res.keys())
    pytest.assume('direction' in res.keys())
    pytest.assume('departure_date' in res.keys())
    pytest.assume('remaining_seats' in res.keys())
