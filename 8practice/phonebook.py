from connect import connect_db

def search_contacts(pattern):
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM search_contacts(%s)", (pattern,))
    rows = cur.fetchall()

    for r in rows:
        print(r)

    cur.close()
    conn.close()

def show_paginated(limit, offset):
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (limit, offset))
    rows = cur.fetchall()

    for r in rows:
        print(r)

    cur.close()
    conn.close()

def add_or_update(name, phone):
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("CALL upsert_contact(%s, %s)", (name, phone))
    conn.commit()

    cur.close()
    conn.close()

def add_many():
    conn = connect_db()
    cur = conn.cursor()

    names = ["Ali", "Bob", "Test"]
    phones = ["111111", "222222", "abc"]  # last one is wrong

    cur.execute("CALL insert_many_contacts(%s, %s)", (names, phones))
    conn.commit()

    cur.close()
    conn.close()

def delete_contact(value):
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("CALL delete_contact(%s)", (value,))
    conn.commit()

    cur.close()
    conn.close()

if __name__ == "__main__":
    add_or_update("Alice", "123456")
    add_or_update("Bob", "987654")

    print("Search result:")
    search_contacts("Ali")

    print("\nPagination:")
    show_paginated(2, 0)

    print("\nInsert many:")
    add_many()

    print("\nDelete:")
    delete_contact("Bob")
