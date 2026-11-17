
import psycopg2
import json
import csv
from pathlib import Path
from contextlib import closing
from config import load_config


BASE_DIR = Path(__file__).parent


def connect():
    config = load_config()
    return psycopg2.connect(**config)


def install_sql():
    with closing(connect()) as conn:
        with conn:
            with conn.cursor() as cur:
                functions = (BASE_DIR / "functions.sql").read_text()
                procedures = (BASE_DIR / "procedures.sql").read_text()

                cur.execute(functions)
                cur.execute(procedures)

    print("Functions and procedures created!")


def get_group_id(cur, group_name):
    if not group_name:
        group_name = "Other"

    cur.execute("""
        INSERT INTO groups(name)
        VALUES (%s)
        ON CONFLICT (name) DO NOTHING;
    """, (group_name,))

    cur.execute(
        "SELECT id FROM groups WHERE name = %s",
        (group_name,)
    )

    return cur.fetchone()[0]


def show_contacts_page():
    try:
        limit = int(input("Contacts per page: "))

        if limit <= 0:
            print("Limit must be greater than zero!")
            return

    except ValueError:
        print("Please enter a number!")
        return

    page = 1

    while True:
        offset = (page - 1) * limit

        with closing(connect()) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT * FROM get_contacts_page(%s, %s)",
                    (limit, offset)
                )

                contacts = cur.fetchall()

        print("\nCONTACTS")

        for contact in contacts:
            print(contact)

        if not contacts:
            print("No contacts on this page!")

        choice = input("\nnext / prev / quit: ").lower()

        if choice == "next":
            if contacts:
                page += 1
            else:
                print("There are no more contacts!")

        elif choice == "prev":
            if page > 1:
                page -= 1
            else:
                print("You are already on the first page!")

        elif choice == "quit":
            break

        else:
            print("Invalid choice!")


def search_contacts():
    query = input("Enter name, email or phone: ")

    with closing(connect()) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM search_contacts(%s)",
                (query,)
            )

            contacts = cur.fetchall()

    if contacts:
        for contact in contacts:
            print(contact)
    else:
        print("No contacts found!")


def filter_by_group():
    group_name = input("Enter group name: ")

    with closing(connect()) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    c.id,
                    c.first_name,
                    c.second_name,
                    c.email,
                    c.birthday,
                    g.name
                FROM contacts c
                LEFT JOIN groups g ON c.group_id = g.id
                WHERE LOWER(g.name) = LOWER(%s)
                ORDER BY c.first_name;
            """, (group_name,))

            contacts = cur.fetchall()

    if contacts:
        for contact in contacts:
            print(contact)
    else:
        print("No contacts found in this group!")


def search_by_email():
    email = input("Enter email or part of email: ")

    with closing(connect()) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, first_name, second_name, email, birthday
                FROM contacts
                WHERE email ILIKE %s
                ORDER BY first_name;
            """, ("%" + email + "%",))

            contacts = cur.fetchall()

    if contacts:
        for contact in contacts:
            print(contact)
    else:
        print("No contacts found!")


def sort_contacts():
    print("\nSort contacts by:")
    print("1. Name")
    print("2. Birthday")
    print("3. Date added")

    choice = input("Choose: ")

    sort_options = {
        "1": "c.first_name",
        "2": "c.birthday NULLS LAST",
        "3": "c.created_at"
    }

    if choice not in sort_options:
        print("Invalid choice!")
        return

    order = sort_options[choice]

    with closing(connect()) as conn:
        with conn.cursor() as cur:
            cur.execute(f"""
                SELECT
                    c.id,
                    c.first_name,
                    c.second_name,
                    c.email,
                    c.birthday,
                    g.name,
                    c.created_at
                FROM contacts c
                LEFT JOIN groups g ON c.group_id = g.id
                ORDER BY {order};
            """)

            contacts = cur.fetchall()

    for contact in contacts:
        print(contact)


def add_or_update_contact():
    first_name = input("First name: ")
    second_name = input("Second name: ")
    phone = input("Phone: ")
    email = input("Email: ") or None
    birthday = input("Birthday (YYYY-MM-DD): ") or None
    group_name = input("Group (Family/Work/Friend/Other): ") or "Other"

    with closing(connect()) as conn:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    "CALL upsert_contact(%s, %s, %s)",
                    (first_name, second_name, phone)
                )

                group_id = get_group_id(cur, group_name)

                cur.execute("""
                    UPDATE contacts
                    SET email = %s,
                        birthday = %s,
                        group_id = %s
                    WHERE first_name = %s
                      AND second_name = %s;
                """, (
                    email,
                    birthday,
                    group_id,
                    first_name,
                    second_name
                ))

    print("Contact saved successfully!")


def bulk_insert_contacts():
    print("Enter contacts as JSON.")
    print('Example: [{"first_name":"Ali","second_name":"Nur","phone":"+77001234567"}]')

    data = input("JSON: ")

    try:
        contacts = json.loads(data)

        if not isinstance(contacts, list):
            print("JSON must contain a list!")
            return

    except json.JSONDecodeError:
        print("Invalid JSON!")
        return

    with closing(connect()) as conn:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    "CALL bulk_insert_contacts(%s, %s)",
                    (json.dumps(contacts), None)
                )

                result = cur.fetchone()
                invalid = result[0] if result else []

    print("Bulk insert completed!")
    print("Invalid contacts:", invalid)


def delete_contact():
    print("\nDelete by:")
    print("1. Name")
    print("2. Phone")

    choice = input("Choose: ")

    if choice == "1":
        value = input("Enter first name: ")
        delete_type = "name"

    elif choice == "2":
        value = input("Enter phone: ")
        delete_type = "phone"

    else:
        print("Invalid choice!")
        return

    with closing(connect()) as conn:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    "CALL delete_contact(%s, %s)",
                    (value, delete_type)
                )

    print("Delete operation completed!")


def add_phone():
    contact_name = input("Enter full name: ")
    phone = input("Enter phone: ")
    phone_type = input("Phone type (home/work/mobile): ").lower()

    if phone_type not in ["home", "work", "mobile"]:
        print("Invalid phone type!")
        return

    with closing(connect()) as conn:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    "CALL add_phone(%s, %s, %s)",
                    (contact_name, phone, phone_type)
                )

    print("Phone added successfully!")


def move_to_group():
    contact_name = input("Enter full name: ")
    group_name = input("Enter new group: ")

    with closing(connect()) as conn:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    "CALL move_to_group(%s, %s)",
                    (contact_name, group_name)
                )

    print("Contact moved successfully!")


def export_json():
    file_name = input("Export file name (default contacts_export.json): ")

    if not file_name:
        file_name = "contacts_export.json"

    contacts = []

    with closing(connect()) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    c.id,
                    c.first_name,
                    c.second_name,
                    c.email,
                    c.birthday,
                    g.name
                FROM contacts c
                LEFT JOIN groups g ON c.group_id = g.id
                ORDER BY c.id;
            """)

            rows = cur.fetchall()

            for row in rows:
                contact_id, first, second, email, birthday, group_name = row

                cur.execute("""
                    SELECT phone, type
                    FROM phones
                    WHERE contact_id = %s
                    ORDER BY id;
                """, (contact_id,))

                phones = cur.fetchall()

                contacts.append({
                    "first_name": first,
                    "second_name": second,
                    "email": email,
                    "birthday": birthday.isoformat() if birthday else None,
                    "group": group_name,
                    "phones": [
                        {"phone": p[0], "type": p[1]}
                        for p in phones
                    ]
                })

    file_path = BASE_DIR / file_name

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(contacts, file, indent=4, ensure_ascii=False)

    print("Contacts exported successfully!")


def import_json():
    file_name = input("Enter JSON file path: ")

    try:
        with open(file_name, "r", encoding="utf-8") as file:
            contacts = json.load(file)

        if not isinstance(contacts, list):
            print("JSON must contain a list!")
            return

    except (FileNotFoundError, json.JSONDecodeError):
        print("File not found or invalid JSON!")
        return

    with closing(connect()) as conn:
        with conn:
            with conn.cursor() as cur:
                for item in contacts:
                    first = item["first_name"]
                    second = item["second_name"]

                    cur.execute("""
                        SELECT id
                        FROM contacts
                        WHERE first_name = %s
                          AND second_name = %s;
                    """, (first, second))

                    existing = cur.fetchone()

                    if existing:
                        print(f"\n{first} {second} already exists.")
                        choice = input("Skip or overwrite? (skip/overwrite): ").lower()

                        if choice == "skip":
                            continue

                        elif choice != "overwrite":
                            print("Invalid choice. Contact skipped.")
                            continue

                        contact_id = existing[0]

                        group_id = get_group_id(
                            cur,
                            item.get("group") or "Other"
                        )

                        cur.execute("""
                            UPDATE contacts
                            SET email = %s,
                                birthday = %s,
                                group_id = %s
                            WHERE id = %s;
                        """, (
                            item.get("email"),
                            item.get("birthday"),
                            group_id,
                            contact_id
                        ))

                        cur.execute(
                            "DELETE FROM phones WHERE contact_id = %s",
                            (contact_id,)
                        )

                    else:
                        group_id = get_group_id(
                            cur,
                            item.get("group") or "Other"
                        )

                        cur.execute("""
                            INSERT INTO contacts
                                (first_name, second_name, email, birthday, group_id)
                            VALUES (%s, %s, %s, %s, %s)
                            RETURNING id;
                        """, (
                            first,
                            second,
                            item.get("email"),
                            item.get("birthday"),
                            group_id
                        ))

                        contact_id = cur.fetchone()[0]

                    for phone_item in item.get("phones", []):
                        cur.execute("""
                            INSERT INTO phones(contact_id, phone, type)
                            VALUES (%s, %s, %s)
                            ON CONFLICT (contact_id, phone) DO NOTHING;
                        """, (
                            contact_id,
                            phone_item["phone"],
                            phone_item.get("type", "mobile")
                        ))

    print("JSON import completed!")


def import_csv():
    file_name = input("Enter CSV file path: ")

    try:
        with open(file_name, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            with closing(connect()) as conn:
                with conn:
                    with conn.cursor() as cur:
                        for row in reader:
                            first = row["first_name"]
                            second = row["second_name"]
                            email = row.get("email") or None
                            birthday = row.get("birthday") or None
                            group_name = row.get("group") or "Other"
                            phone = row.get("phone")
                            phone_type = row.get("phone_type") or "mobile"

                            group_id = get_group_id(cur, group_name)

                            cur.execute("""
                                INSERT INTO contacts
                                    (first_name, second_name, email, birthday, group_id)
                                VALUES (%s, %s, %s, %s, %s)
                                ON CONFLICT (first_name, second_name)
                                DO UPDATE SET
                                    email = EXCLUDED.email,
                                    birthday = EXCLUDED.birthday,
                                    group_id = EXCLUDED.group_id
                                RETURNING id;
                            """, (
                                first,
                                second,
                                email,
                                birthday,
                                group_id
                            ))

                            contact_id = cur.fetchone()[0]

                            if phone:
                                cur.execute("""
                                    INSERT INTO phones(contact_id, phone, type)
                                    VALUES (%s, %s, %s)
                                    ON CONFLICT (contact_id, phone) DO NOTHING;
                                """, (
                                    contact_id,
                                    phone,
                                    phone_type
                                ))

        print("CSV import completed!")

    except FileNotFoundError:
        print("File not found!")

    except (KeyError, ValueError) as error:
        print("CSV data error:", error)


def main():
    install_sql()

    while True:
        print("\n========== PHONEBOOK ==========")
        print("1. Search contacts")
        print("2. Show contacts with pagination")
        print("3. Filter by group")
        print("4. Search by email")
        print("5. Sort contacts")
        print("6. Add or update contact")
        print("7. Bulk insert contacts")
        print("8. Delete contact")
        print("9. Add phone")
        print("10. Move contact to group")
        print("11. Export contacts to JSON")
        print("12. Import contacts from JSON")
        print("13. Import contacts from CSV")
        print("0. Exit")

        choice = input("\nChoose an option: ")

        if choice == "1":
            search_contacts()

        elif choice == "2":
            show_contacts_page()

        elif choice == "3":
            filter_by_group()

        elif choice == "4":
            search_by_email()

        elif choice == "5":
            sort_contacts()

        elif choice == "6":
            add_or_update_contact()

        elif choice == "7":
            bulk_insert_contacts()

        elif choice == "8":
            delete_contact()

        elif choice == "9":
            add_phone()

        elif choice == "10":
            move_to_group()

        elif choice == "11":
            export_json()

        elif choice == "12":
            import_json()

        elif choice == "13":
            import_csv()

        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()