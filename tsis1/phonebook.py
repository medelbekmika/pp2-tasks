import csv
import json
import os
import sys
from datetime import date, datetime
import psycopg2
from connect import get_connection
#  HELPERS
def clear():
    os.system("cls" if os.name == "nt" else "clear")

def pause():
    input("\nPress Enter to continue...")

def print_header(title: str):
    print("\n" + "═" * 55)
    print(f"  {title}")
    print("═" * 55)

def json_serial(obj):
    """JSON serializer for date / datetime objects."""
    if isinstance(obj, (date, datetime)):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")
#  SCHEMA INITIALISATION 
def init_schema():
    """Applies schema.sql and procedures.
    sql to the database."""
    conn = get_connection()
    cur  = conn.cursor()
    base_dir = os.path.dirname(os.path.abspath(__file__))

    for filename in ("schema.sql", "procedures.sql"):
        filepath = os.path.join(base_dir, filename)
        if not os.path.exists(filepath):
            print(f"[WARNING] {filename} not found — skipping.")
            continue
        with open(filepath, "r", encoding="utf-8") as f:
            sql = f.read()
        try:
            cur.execute(sql)
            conn.commit()
            print(f"[OK] {filename} applied.")
        except Exception as e:
            conn.rollback()
            print(f"[ERROR] {filename}: {e}")

    cur.close()
    conn.close()
#  3.4  STORED PROCEDURE CALLERS
def call_add_phone(contact_name: str, phone: str, phone_type: str):
    """Calls the PL/pgSQL procedure add_phone."""
    conn = get_connection()
    cur  = conn.cursor()
    try:
        cur.execute("CALL add_phone(%s, %s, %s);", (contact_name, phone, phone_type))
        conn.commit()
        print(f"[OK] Phone {phone} ({phone_type}) added to '{contact_name}'.")
    except psycopg2.Error as e:
        conn.rollback()
        print(f"[ERROR] {e.pgerror or e}")
    finally:
        cur.close()
        conn.close()

def call_move_to_group(contact_name: str, group_name: str):
    """Calls the PL/pgSQL procedure move_to_group."""
    conn = get_connection()
    cur  = conn.cursor()
    try:
        cur.execute("CALL move_to_group(%s, %s);", (contact_name, group_name))
        conn.commit()
        print(f"[OK] Contact '{contact_name}' moved to group '{group_name}'.")
    except psycopg2.Error as e:
        conn.rollback()
        print(f"[ERROR] {e.pgerror or e}")
    finally:
        cur.close()
        conn.close()

def call_search_contacts(query: str):
    """Calls the PL/pgSQL function search_contacts and prints results."""
    conn = get_connection()
    cur  = conn.cursor()
    try:
        cur.execute("SELECT * FROM search_contacts(%s);", (query,))
        rows = cur.fetchall()
        if not rows:
            print("  No results found.")
            return
        print(f"\n  Found: {len(rows)} contact(s)\n")
        print(f"  {'Username':<15} {'First':<12} {'Last':<12} {'Email':<22} {'Group':<10} Phones")
        print("  " + "-" * 90)
        for row in rows:
            _, username, fn, ln, email, bday, grp, phones = row
            fn     = fn     or ""
            ln     = ln     or ""
            email  = email  or ""
            grp    = grp    or ""
            phones = phones or ""
            print(f"  {username:<15} {fn:<12} {ln:<12} {email:<22} {grp:<10} {phones}")
    except psycopg2.Error as e:
        print(f"[ERROR] {e}")
    finally:
        cur.close()
        conn.close()
#  3.2  ADVANCED SEARCH & FILTER
def get_groups() -> list:
    """Returns all groups as [(id, name), ...]."""
    conn = get_connection()
    cur  = conn.cursor()
    cur.execute("SELECT id, name FROM groups ORDER BY name;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def filter_by_group():
    """Shows contacts that belong to a chosen group."""
    print_header("FILTER BY GROUP")
    groups = get_groups()
    print("  Available groups:")
    for i, (_, gname) in enumerate(groups, 1):
        print(f"    {i}. {gname}")

    choice = input("\n  Enter group number (or Enter to cancel): ").strip()
    if not choice:
        return
    try:
        group_id, group_name = groups[int(choice) - 1]
    except (ValueError, IndexError):
        print("[ERROR] Invalid choice.")
        return

    sort_col = _ask_sort_order()
    conn = get_connection()
    cur  = conn.cursor()
    cur.execute(f"""
        SELECT c.username, c.firstname, c.lastname, c.email, c.birthday,
               STRING_AGG(p.phone || ' (' || p.type || ')', ', ') AS phones
        FROM contacts c
        LEFT JOIN phones p ON c.id = p.contact_id
        WHERE c.group_id = %s
        GROUP BY c.id, c.username, c.firstname, c.lastname, c.email, c.birthday
        ORDER BY {sort_col};
    """, (group_id,))
    rows = cur.fetchall()
    cur.close()
    conn.close()

    print(f"\n  Group: {group_name}  |  Contacts: {len(rows)}\n")
    _print_contacts_table(rows)

def search_by_email():
    """Partial-match search on the email field."""
    print_header("SEARCH BY EMAIL")
    query = input("  Enter part of the email (e.g. gmail): ").strip()
    if not query:
        return

    conn = get_connection()
    cur  = conn.cursor()
    cur.execute("""
        SELECT c.username, c.firstname, c.lastname, c.email, c.birthday,
               STRING_AGG(p.phone || ' (' || p.type || ')', ', ') AS phones
        FROM contacts c
        LEFT JOIN phones p ON c.id = p.contact_id
        WHERE c.email ILIKE %s
        GROUP BY c.id, c.username, c.firstname, c.lastname, c.email, c.birthday
        ORDER BY c.username;
    """, (f"%{query}%",))
    rows = cur.fetchall()
    cur.close()
    conn.close()

    print(f"\n  Found: {len(rows)}\n")
    _print_contacts_table(rows)

def _ask_sort_order() -> str:
    """Prompts the user for sort order and returns a safe SQL column."""
    print("\n  Sort by:")
    print("    1. Name (username)")
    print("    2. Birthday")
    print("    3. Date added")
    choice = input("  Choice [1-3, Enter=1]: ").strip()
    mapping = {
        "1": "c.username",
        "2": "c.birthday NULLS LAST",
        "3": "c.created_at",
    }
    return mapping.get(choice, "c.username")

def _print_contacts_table(rows):
    """Prints a formatted contact table to the console."""
    if not rows:
        print("  No data.")
        return
    print(f"  {'Username':<15} {'First':<12} {'Last':<12} {'Email':<22} {'Birthday':<12} Phones")
    print("  " + "-" * 95)
    for row in rows:
        username, fn, ln, email, bday, phones = row
        fn     = fn     or "—"
        ln     = ln     or "—"
        email  = email  or "—"
        bday   = str(bday) if bday else "—"
        phones = phones or "—"
        print(f"  {username:<15} {fn:<12} {ln:<12} {email:<22} {bday:<12} {phones}")
#  3.2  PAGINATED NAVIGATION
def paginated_browse():
    """
    Paginated contact browser with next / prev / quit navigation.
    Uses LIMIT / OFFSET (the DB function from Practice 8 is kept on
    the server side; here we drive it from the console).
    """
    print_header("BROWSE CONTACTS  (paginated)")
    sort_col  = _ask_sort_order()
    page_size = 5
    offset    = 0

    while True:
        conn = get_connection()
        cur  = conn.cursor()
        cur.execute(f"""
            SELECT c.username, c.firstname, c.lastname, c.email, c.birthday,
                   STRING_AGG(p.phone || ' (' || p.type || ')', ', ') AS phones
            FROM contacts c
            LEFT JOIN phones p ON c.id = p.contact_id
            GROUP BY c.id, c.username, c.firstname, c.lastname, c.email, c.birthday
            ORDER BY {sort_col}
            LIMIT %s OFFSET %s;
        """, (page_size, offset))
        rows = cur.fetchall()

        cur.execute("SELECT COUNT(*) FROM contacts;")
        total = cur.fetchone()[0]
        cur.close()
        conn.close()

        clear()
        page_num    = offset // page_size + 1
        total_pages = max((total + page_size - 1) // page_size, 1)
        print(f"\n  Page {page_num} of {total_pages}  (total contacts: {total})\n")
        _print_contacts_table(rows)

        print("\n  [next] Next page   [prev] Previous page   [quit] Exit")
        cmd = input("  Command: ").strip().lower()

        if cmd in ("quit", "q"):
            break
        elif cmd in ("next", "n"):
            if offset + page_size < total:
                offset += page_size
            else:
                print("  You are already on the last page.")
                pause()
        elif cmd in ("prev", "p"):
            if offset >= page_size:
                offset -= page_size
            else:
                print("  You are already on the first page.")
                pause()
        else:
            print("  Unknown command.")
            pause()
#  3.3  EXPORT TO JSON
def export_to_json():
    """Exports all contacts (with phones and group) to a JSON file."""
    print_header("EXPORT TO JSON")
    filename = input("  Output file name [contacts.json]: ").strip() or "contacts.json"

    conn = get_connection()
    cur  = conn.cursor()
    cur.execute("""
        SELECT c.id, c.username, c.firstname, c.lastname,
               c.email, c.birthday, g.name AS group_name, c.created_at
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        ORDER BY c.username;
    """)
    contact_rows = cur.fetchall()

    contacts_list = []
    for row in contact_rows:
        cid, username, fn, ln, email, bday, grp, created = row
        cur.execute("SELECT phone, type FROM phones WHERE contact_id = %s;", (cid,))
        phone_rows = cur.fetchall()
        contacts_list.append({
            "username":   username,
            "firstname":  fn,
            "lastname":   ln,
            "email":      email,
            "birthday":   bday,
            "group":      grp,
            "created_at": created,
            "phones": [{"phone": p, "type": t} for p, t in phone_rows],
        })

    cur.close()
    conn.close()

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(contacts_list, f, ensure_ascii=False, indent=2, default=json_serial)

    print(f"  [OK] {len(contacts_list)} contacts exported → {filename}")
#  3.3  IMPORT FROM JSON
def import_from_json():
    """Reads contacts from a JSON file and inserts them into the DB.
    On duplicate username, asks the user: skip or overwrite."""
    print_header("IMPORT FROM JSON")
    filename = input("  Path to JSON file [contacts.json]: ").strip() or "contacts.json"

    if not os.path.exists(filename):
        print(f"  [ERROR] File '{filename}' not found.")
        return

    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)

    conn = get_connection()
    cur  = conn.cursor()
    inserted = skipped = overwritten = 0

    for item in data:
        username = item.get("username", "").strip()
        if not username:
            print("  [SKIP] Contact has no username.")
            skipped += 1
            continue

        firstname  = item.get("firstname")
        lastname   = item.get("lastname")
        email      = item.get("email")
        birthday   = item.get("birthday")
        group_name = item.get("group")
        phones     = item.get("phones", [])

        group_id = None
        if group_name:
            cur.execute("SELECT id FROM groups WHERE name = %s;", (group_name,))
            row = cur.fetchone()
            if row:
                group_id = row[0]
            else:
                cur.execute(
                    "INSERT INTO groups (name) VALUES (%s) RETURNING id;", (group_name,)
                )
                group_id = cur.fetchone()[0]
        cur.execute("SELECT id FROM contacts WHERE username = %s;", (username,))
        existing = cur.fetchone()

        if existing:
            print(f"\n  Contact '{username}' already exists.")
            action = input("  [s] Skip   [o] Overwrite: ").strip().lower()
            if action == "o":
                cur.execute("""
                    UPDATE contacts
                    SET firstname=%s, lastname=%s, email=%s, birthday=%s, group_id=%s
                    WHERE username=%s;
                """, (firstname, lastname, email, birthday, group_id, username))
                contact_id = existing[0]
                cur.execute("DELETE FROM phones WHERE contact_id = %s;", (contact_id,))
                for ph in phones:
                    cur.execute(
                        "INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s);",
                        (contact_id, ph.get("phone"), ph.get("type", "mobile"))
                    )
                overwritten += 1
                print(f"  → Overwritten: {username}")
            else:
                skipped += 1
                print(f"  → Skipped: {username}")
            continue
        cur.execute("""
            INSERT INTO contacts (username, firstname, lastname, email, birthday, group_id)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id;
        """, (username, firstname, lastname, email, birthday, group_id))
        contact_id = cur.fetchone()[0]

        for ph in phones:
            cur.execute(
                "INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s);",
                (contact_id, ph.get("phone"), ph.get("type", "mobile"))
            )
        inserted += 1

    conn.commit()
    cur.close()
    conn.close()
    print(f"\n  [DONE] Inserted: {inserted}  |  Overwritten: {overwritten}  |  Skipped: {skipped}")
#  3.3  EXTENDED CSV IMPORT  (new fields: email, birthday, group, type)
def import_from_csv():
    """Extended CSV import (extends Practice 7).
    Expected columns: username, firstname, lastname, phone, type, email, birthday, group
    """
    print_header("IMPORT FROM CSV  (extended)")
    filename = input("  Path to CSV file [contacts.csv]: ").strip() or "contacts.csv"

    if not os.path.exists(filename):
        print(f"  [ERROR] File '{filename}' not found.")
        return

    conn = get_connection()
    cur  = conn.cursor()
    inserted = skipped = errors = 0

    with open(filename, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            username = row.get("username", "").strip()
            if not username:
                errors += 1
                continue

            phone      = row.get("phone",     "").strip() or None
            phone_type = row.get("type",      "mobile").strip() or "mobile"
            email      = row.get("email",     "").strip() or None
            birthday   = row.get("birthday",  "").strip() or None
            group_name = row.get("group",     "").strip() or None
            firstname  = row.get("firstname", "").strip() or None
            lastname   = row.get("lastname",  "").strip() or None

            if phone_type not in ("home", "work", "mobile"):
                phone_type = "mobile"
            group_id = None
            if group_name:
                cur.execute("SELECT id FROM groups WHERE name = %s;", (group_name,))
                r = cur.fetchone()
                if r:
                    group_id = r[0]
                else:
                    cur.execute(
                        "INSERT INTO groups (name) VALUES (%s) RETURNING id;", (group_name,)
                    )
                    group_id = cur.fetchone()[0]
            cur.execute("SELECT id FROM contacts WHERE username = %s;", (username,))
            if cur.fetchone():
                skipped += 1
                continue

            cur.execute("""
                INSERT INTO contacts (username, firstname, lastname, email, birthday, group_id)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id;
            """, (username, firstname, lastname, email, birthday, group_id))
            contact_id = cur.fetchone()[0]

            if phone:
                cur.execute(
                    "INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s);",
                    (contact_id, phone, phone_type)
                )
            inserted += 1

    conn.commit()
    cur.close()
    conn.close()
    print(f"\n  [DONE] Inserted: {inserted}  |  Skipped (duplicates): {skipped}  |  Errors: {errors}")
#  MENU ACTIONS — add phone & move to group
def menu_add_phone():
    print_header("ADD PHONE TO CONTACT")
    name  = input("  Contact username: ").strip()
    phone = input("  Phone number: ").strip()
    print("  Type:  [1] mobile   [2] home   [3] work")
    t = input("  Choice [1]: ").strip()
    phone_type = {"1": "mobile", "2": "home", "3": "work"}.get(t, "mobile")
    call_add_phone(name, phone, phone_type)


def menu_move_to_group():
    print_header("MOVE CONTACT TO GROUP")
    name = input("  Contact username: ").strip()
    print("  Existing groups:")
    for _, gname in get_groups():
        print(f"    - {gname}")
    group = input("  Group name (or type a new one): ").strip()
    call_move_to_group(name, group)


def menu_search():
    print_header("SEARCH CONTACTS  (name / phone / email)")
    query = input("  Search query: ").strip()
    call_search_contacts(query)
#  MAIN MENU
MENU = """
  ┌─────────────────────────────────────────────┐
  │        PhoneBook Extended  —  TSIS 1        │
  ├─────────────────────────────────────────────┤
  │  1. Browse contacts  (paginated)            │
  │  2. Filter by group                         │
  │  3. Search  (name / phone / email)          │
  │  4. Search by email                         │
  │  5. Add phone to a contact                  │
  │  6. Move contact to a group                 │
  │─────────────────────────────────────────────│
  │  7. Import from CSV                         │
  │  8. Import from JSON                        │
  │  9. Export to JSON                          │
  │─────────────────────────────────────────────│
  │  0. Exit                                    │
  └─────────────────────────────────────────────┘
"""

ACTIONS = {
    "1": paginated_browse,
    "2": filter_by_group,
    "3": menu_search,
    "4": search_by_email,
    "5": menu_add_phone,
    "6": menu_move_to_group,
    "7": import_from_csv,
    "8": import_from_json,
    "9": export_to_json,
}


def main():
    print("\n  Initialising database schema...")
    init_schema()
    print("  Ready!\n")

    while True:
        print(MENU)
        choice = input("  Select an option: ").strip()
        if choice == "0":
            print("  Goodbye!\n")
            sys.exit(0)
        action = ACTIONS.get(choice)
        if action:
            action()
            pause()
        else:
            print("  Invalid choice, please try again.")


if __name__ == "__main__":
    main()
