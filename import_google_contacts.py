import pandas as pd
import sqlite3
from pandas import isna

DB_PATH = "prm.db"
ODS_FILE = "contacts.ods"  # Replace with your actual .ods file path

def clean_phone(phone_raw):
    if isna(phone_raw):
        return None
    # Convert ::: separated values to comma-separated and strip whitespace
    phones = [p.strip() for p in str(phone_raw).split(":::") if p.strip()]
    return ", ".join(phones) if phones else None

def import_contacts(ods_path, db_path):
    df = pd.read_excel(ods_path, engine='odf')
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    count = 0
    for _, row in df.iterrows():
        first_name = str(row.get('first_name')).strip() if not isna(row.get('first_name')) else None
        last_name = str(row.get('last_name')).strip() if not isna(row.get('last_name')) else None
        email = str(row.get('email')).strip() if not isna(row.get('email')) else None
        photo_url = str(row.get('Photo')).strip() if not isna(row.get('Photo')) else None
        phone = clean_phone(row.get('phone1'))

        # Skip row if it has no usable data
        if all(isna(v) or str(v).strip() == '' for v in [first_name, email, phone]):
            continue

        try:
            cursor.execute("""
                INSERT OR IGNORE INTO contacts (first_name, last_name, email, phone, photo_url, source)
                VALUES (?, ?, ?, ?, ?, 'imported_ods')
            """, (first_name, last_name, email, phone, photo_url))
            count += 1
        except Exception as e:
            print(f"⚠️ Error inserting row: {e}")

    conn.commit()
    conn.close()
    print(f"✅ Successfully imported {count} contacts.")

if __name__ == "__main__":
    import_contacts(ODS_FILE, DB_PATH)
