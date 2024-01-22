import unittest
import requests
import psycopg2
import pytest
from time import sleep


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
        r = requests.get("http://localhost:8000/health")
        self.assertEqual(r.status_code, 200)

    def test_ticket_service_connection(self):
        r = requests.get("http://localhost:8001/health")
        self.assertEqual(r.status_code, 200)


if __name__ == '__main__':
    unittest.main()
