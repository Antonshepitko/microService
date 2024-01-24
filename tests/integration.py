import unittest
import pytest
import requests
import psycopg2
from datetime import datetime
from time import sleep
from uuid import uuid4

station_url = 'https://localhost:8000'
ticket_url = 'https://localhost:8001'
add_train_url = f'{station_url}/add_train'
get_train_by_id_url = f'{station_url}/get_train_by_id/'

train_data = {
    "id": str(uuid4()),
    "model": "TrainModel123",
    "direction": "SomeDirection",
    "departure_date": str(datetime.now()),
    "remaining_seats": 50
}


def check_connect():
    try:
        conn = psycopg2.connect(
            dbname='RailRoad',
            user='postgres',
            password='micro6',
            host='localhost',
            port='5432'
        )
        conn.close()
        return True
    except:
        return False


class TestIntegration(unittest.TestCase):
    # CMD: python tests/integration.py

    def test_db_connection(self):
        sleep(5)
        self.assertEqual(check_connect(), True)

    def test_station_service_connection(self):
        r = requests.get(f"{station_url}/health")
        self.assertEqual(r.status_code, 200)

    def test_ticket_service_connection(self):
        r = requests.get(f"{ticket_url}/health")
        self.assertEqual(r.status_code, 200)

    def test_get_train(self):
        res = requests.get(f"{get_train_by_id_url}/86f053a0-0dd1-4439-ba43-bdf586220bd2")
        res = json.loads(res.text)[0]
        pytest.assume(res['model'] == 'Test')
        pytest.assume(res['direction'] == 'St. Petersburg')


if __name__ == '__main__':
    unittest.main()
