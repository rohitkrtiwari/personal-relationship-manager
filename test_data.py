import sqlite3

conn = sqlite3.connect('prm.db')
cursor = conn.cursor()

# Check table structure
cursor.execute("PRAGMA table_info(contacts)")
print("Table structure:")
for column in cursor.fetchall():
    print(column)

# Check first 5 records
cursor.execute("SELECT * FROM contacts LIMIT 5")
print("\nFirst 5 records:")
for row in cursor.fetchall():
    print(row)

conn.close()