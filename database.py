import sqlite3
from sqlite3 import Error

def create_connection():
    """Create a SQLite database connection."""
    conn = None
    try:
        conn = sqlite3.connect("prm.db")  # File will auto-create
        print("Database connection established.")
        return conn
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None

def create_tables(conn):
    """Create all tables for the PRM."""
    sql_contacts = """
    CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT,
        email TEXT UNIQUE,
        phone TEXT,
        photo_url TEXT,
        source TEXT DEFAULT 'manual'
    );
    """

    sql_tags = """
    CREATE TABLE IF NOT EXISTS tags (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL
    );
    """

    sql_contact_tags = """
    CREATE TABLE IF NOT EXISTS contact_tags (
        contact_id INTEGER,
        tag_id INTEGER,
        FOREIGN KEY (contact_id) REFERENCES contacts (id) ON DELETE CASCADE,
        FOREIGN KEY (tag_id) REFERENCES tags (id) ON DELETE CASCADE,
        PRIMARY KEY (contact_id, tag_id)
    );
    """

    cursor = conn.cursor()
    cursor.execute(sql_contacts)
    cursor.execute(sql_tags)
    cursor.execute(sql_contact_tags)
    conn.commit()
    print("Tables created: contacts, tags, contact_tags")

def add_tag(conn, name):
    """Add a new tag to the database."""
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO tags (name) VALUES (?)", (name,))
    conn.commit()
    print(f"Tag added: {name}")

def remove_tag_from_contact(conn, contact_id, tag_name):
    """Unassign a tag from a contact."""
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM contact_tags 
        WHERE contact_id = ? 
        AND tag_id = (SELECT id FROM tags WHERE name = ?)
    """, (contact_id, tag_name))
    conn.commit()
    print(f"Removed tag '{tag_name}' from contact ID {contact_id}")

def get_all_tags(conn):
    """Fetch all tags from the database."""
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM tags")
    return [tag[0] for tag in cursor.fetchall()]

def assign_tag_to_contact(conn, contact_id, tag_name):
    cursor = conn.cursor()
    # Check if contact exists
    cursor.execute("SELECT id FROM contacts WHERE id = ?", (contact_id,))
    if not cursor.fetchone():
        print(f"Error: Contact ID {contact_id} does not exist!")
        return
    # Ensure the tag exists
    cursor.execute("INSERT OR IGNORE INTO tags (name) VALUES (?)", (tag_name,))
    # Get tag ID
    cursor.execute("SELECT id FROM tags WHERE name = ?", (tag_name,))
    tag_id = cursor.fetchone()[0]
    # Assign the tag
    cursor.execute(
        "INSERT OR IGNORE INTO contact_tags (contact_id, tag_id) VALUES (?, ?)",
        (contact_id, tag_id)
    )
    conn.commit()
    print(f"Assigned tag '{tag_name}' to contact ID {contact_id}")

def get_contacts_by_tag(conn, tag_name):
    """List all contacts with a specific tag."""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT c.id, c.first_name, c.last_name 
        FROM contacts c
        JOIN contact_tags ct ON c.id = ct.contact_id
        JOIN tags t ON ct.tag_id = t.id
        WHERE t.name = ?
    """, (tag_name,))
    return cursor.fetchall()

if __name__ == "__main__":
    conn = create_connection()
    if conn:
        create_tables(conn)
        conn.close()
