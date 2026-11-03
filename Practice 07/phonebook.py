import psycopg2
import csv
from config import load_config


def insert_from_csv():
    command = """
        INSERT INTO phonebook(first_name, second_name, phone)
        VALUES (%s, %s, %s)
    """

    try:
        config = load_config()

        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                with open('contacts.csv', 'r') as file:
                    reader = csv.DictReader(file)

                    for row in reader:
                        cur.execute(command, (
                            row['first_name'],
                            row['second_name'],
                            row['phone']
                        ))

        print("Contacts imported successfully!")

    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


if __name__ == '__main__':
    insert_from_csv()