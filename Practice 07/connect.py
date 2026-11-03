
import psycopg2
from config import load_config


def connect():
    config = load_config()

    try:
        conn = psycopg2.connect(**config)
        print('Connected to the PostgreSQL server!')
        return conn

    except psycopg2.DatabaseError as error:
        print(error)


if __name__ == '__main__':
    connect()
