import psycopg2
import json
from pathlib import Path
from config import load_config

def install_sql():
    config = load_config()

    with psycopg2.connect(**config) as conn:
        with conn.cursor() as cur:
            functions = Path("functions.sql").read_text()
            procedures = Path("procedures.sql").read_text()

            cur.execute(functions)
            cur.execute(procedures)

    print("Functions and procedures created!")

def search_contacts():
    pattern = input("Enter name, surname or phone: ")

    config = load_config()

    with psycopg2.connect(**config) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM get_contacts_by_pattern(%s)",
                (pattern,)
            )

            contacts = cur.fetchall()

            for contact in contacts:
                print(contact)

            if not contacts:
                print("No contacts found!")

def upsert_contact():
    first = input("First name: ")
    second = input("Second name: ")
    phone = input("Phone: ")

    config = load_config()

    with psycopg2.connect(**config) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "CALL upsert_contact(%s, %s, %s)",
                (first, second, phone)
            )

    print("Contact inserted or updated!")

def bulk_insert():
    contacts = []

    count = int(input("How many contacts do you want to add? "))

    for i in range(count):
        print("\nContact", i + 1)

        first = input("First name: ")
        second = input("Second name: ")
        phone = input("Phone: ")

        contacts.append({
            "first_name": first,
            "second_name": second,
            "phone": phone
        })

    config = load_config()

    with psycopg2.connect(**config) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "CALL bulk_insert_contacts(%s, NULL)",
                (json.dumps(contacts),)
            )

            result = cur.fetchone()

            print("\nIncorrect contacts:")
            print(result[0])

def show_contacts():
    limit = int(input("Number of contacts per page: "))
    page = int(input("Page number: "))

    offset = (page - 1) * limit

    config = load_config()

    with psycopg2.connect(**config) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM get_contacts_page(%s, %s)",
                (limit, offset)
            )

            contacts = cur.fetchall()

            for contact in contacts:
                print(contact)

            if not contacts:
                print("No contacts on this page!")

def remove_contact():
    choice = input("Delete by name or phone? ")

    if choice == 'name':
        value = input("First name: ")

    elif choice == 'phone':
        value = input("Phone: ")

    else:
        print("Invalid choice!")
        return

    config = load_config()

    with psycopg2.connect(**config) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "CALL delete_contact(%s, %s)",
                (value, choice)
            )

    print("Delete operation completed!")

def main():
    install_sql()

    while True:
        print("\nPHONEBOOK")
        print("1. Search contacts")
        print("2. Insert or update contact")
        print("3. Insert many contacts")
        print("4. Show contacts with pagination")
        print("5. Delete contact")
        print("0. Exit")

        choice = input("Choose: ")

        if choice == '1':
            search_contacts()

        elif choice == '2':
            upsert_contact()

        elif choice == '3':
            bulk_insert()

        elif choice == '4':
            show_contacts()

        elif choice == '5':
            remove_contact()

        elif choice == '0':
            break

        else:
            print("Invalid choice!")


if __name__ == '__main__':
    main()
