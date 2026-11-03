import psycopg2
import csv
from config import load_config


def insert_from_csv():
    command = "INSERT INTO phonebook(first_name, second_name, phone) VALUES (%s, %s, %s)"

    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                with open('contacts.csv', 'r') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        cur.execute(command, (row['first_name'], row['second_name'], row['phone']))

        print("Contacts imported!")

    except Exception as error:
        print(error)


def insert_from_console():
    first = input("First name: ")
    second = input("Second name: ")
    phone = input("Phone: ")

    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO phonebook(first_name, second_name, phone) VALUES (%s, %s, %s)",
                    (first, second, phone)
                )
        print("Contact added!")

    except Exception as error:
        print(error)


def update_contact():
    contact_id = input("Contact ID: ")
    choice = input("1. Update name\n2. Update phone\nChoose: ")

    if choice == '1':
        value = input("New first name: ")
        command = "UPDATE phonebook SET first_name = %s WHERE id = %s"
    elif choice == '2':
        value = input("New phone: ")
        command = "UPDATE phonebook SET phone = %s WHERE id = %s"
    else:
        print("Invalid choice!")
        return

    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(command, (value, contact_id))
                print("Updated!" if cur.rowcount > 0 else "Contact not found!")

    except Exception as error:
        print(error)


def query_contacts():
    choice = input("1. Search by name\n2. Search by phone prefix\nChoose: ")

    if choice == '1':
        value = '%' + input("Name: ") + '%'
        command = "SELECT * FROM phonebook WHERE first_name ILIKE %s"
    elif choice == '2':
        value = input("Phone prefix: ") + '%'
        command = "SELECT * FROM phonebook WHERE phone LIKE %s"
    else:
        print("Invalid choice!")
        return

    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(command, (value,))
                contacts = cur.fetchall()

                for contact in contacts:
                    print(contact)

                if not contacts:
                    print("No contacts found!")

    except Exception as error:
        print(error)


def delete_contact():
    choice = input("1. Delete by name\n2. Delete by phone\nChoose: ")

    if choice == '1':
        value = input("First name: ")
        command = "DELETE FROM phonebook WHERE first_name = %s"
    elif choice == '2':
        value = input("Phone: ")
        command = "DELETE FROM phonebook WHERE phone = %s"
    else:
        print("Invalid choice!")
        return

    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(command, (value,))
                print("Deleted!" if cur.rowcount > 0 else "Contact not found!")

    except Exception as error:
        print(error)


def main():
    while True:
        print("\n1. Import CSV\n2. Add contact\n3. Update contact")
        print("4. Search contacts\n5. Delete contact\n0. Exit")

        choice = input("Choose: ")

        if choice == '1':
            insert_from_csv()
        elif choice == '2':
            insert_from_console()
        elif choice == '3':
            update_contact()
        elif choice == '4':
            query_contacts()
        elif choice == '5':
            delete_contact()
        elif choice == '0':
            break
        else:
            print("Invalid choice!")


if __name__ == '__main__':
    main()