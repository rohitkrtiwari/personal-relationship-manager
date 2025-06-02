import argparse
from database import *
from tabulate import tabulate
from textwrap import shorten


def add_contact(first_name, last_name=None, email=None, phone=None, photo_url=None):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO contacts 
        (first_name, last_name, email, phone, photo_url) 
        VALUES (?, ?, ?, ?, ?)""",
        (first_name, last_name, email, phone, photo_url)
    )
    conn.commit()
    conn.close()
    print(f"Added contact: {first_name} {last_name}")


def list_contacts():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contacts")
    contacts = cursor.fetchall()
    conn.close()
    for contact in contacts:
        print(contact)


def list_tags_command():
    conn = create_connection()
    if conn:
        tags = get_all_tags(conn)
        conn.close()
        if tags:
            print("All tags:")
            for tag in tags:
                print(f"  - {tag}")
        else:
            print("No tags found.")

def add_tag_command(name):
    conn = create_connection()
    if conn:
        add_tag(conn, name)
        conn.close()

def assign_tag_command(contact_id, tag_name):
    conn = create_connection()
    if conn:
        assign_tag_to_contact(conn, contact_id, tag_name)
        conn.close()

def list_by_tag_command(tag_name):
    conn = create_connection()
    if conn:
        contacts = get_contacts_by_tag(conn, tag_name)
        conn.close()
        if contacts:
            print(f"Contacts with tag '{tag_name}':")
            for contact in contacts:
                print(f"  ID: {contact[0]}, Name: {contact[1]} {contact[2]}")
        else:
            print(f"No contacts found with tag '{tag_name}'.")

def remove_tag_command(contact_id, tag_name):
    conn = create_connection()
    if conn:
        remove_tag_from_contact(conn, contact_id, tag_name)
        conn.close()


def search_contacts(*query_terms):
    conn = create_connection()
    cursor = conn.cursor()
    
    base_query = """
    SELECT * FROM contacts 
    WHERE 1=1
    """
    params = []
    
    for term in query_terms:
        # Check for tag searches (e.g., "tag:work")
        if term.startswith("tag:"):
            tag_name = term[4:].strip()
            base_query += """
            AND id IN (
                SELECT contact_id FROM contact_tags 
                WHERE tag_id = (SELECT id FROM tags WHERE name LIKE ?)
            )
            """
            params.append(f"%{tag_name}%")
        else:
            # Search across name/email/phone
            base_query += """
            AND (
                first_name LIKE ? 
                OR last_name LIKE ? 
                OR email LIKE ? 
                OR phone LIKE ?
            )
            """
            params.extend([f"%{term}%"] * 4)  # Add 4 placeholders
    
    cursor.execute(base_query, params)
    contacts = cursor.fetchall()
    conn.close()
    return contacts




def main():
    parser = argparse.ArgumentParser(description="Personal Relationship Manager (CLI)")
    subparsers = parser.add_subparsers(dest="command")

    # Add contact command
    add_parser = subparsers.add_parser("add", help="Add a new contact")
    add_parser.add_argument("--first-name", required=True, help="First name")
    add_parser.add_argument("--last-name", help="Last name")
    add_parser.add_argument("--email", help="Email address")
    add_parser.add_argument("--phone", help="Phone number")
    add_parser.add_argument("--photo-url", help="URL of profile photo")

    # List contacts command
    subparsers.add_parser("list", help="List all contacts")

    # Add tag command
    tag_parser = subparsers.add_parser("add-tag", help="Create a new tag")
    tag_parser.add_argument("--name", required=True, help="Tag name")

    # Remove Tag:
    remove_parser = subparsers.add_parser("remove-tag", help="Remove a tag from a contact")
    remove_parser.add_argument("--contact-id", type=int, required=True, help="Contact ID")
    remove_parser.add_argument("--tag", required=True, help="Tag name")

    # Assign tag command
    assign_parser = subparsers.add_parser("assign-tag", help="Assign a tag to a contact")
    assign_parser.add_argument("--contact-id", type=int, required=True, help="Contact ID")
    assign_parser.add_argument("--tag", required=True, help="Tag name")

    # List by tag command
    list_tag_parser = subparsers.add_parser("list-by-tag", help="List contacts by tag")
    list_tag_parser.add_argument("--tag", required=True, help="Tag name")

    # Add to subparsers in main():
    list_tags_parser = subparsers.add_parser("list-tags", help="List all tags")

    # search comand
    search_parser = subparsers.add_parser("search", help="Multi-term search")
    search_parser.add_argument(
        "query_terms", 
        nargs="+",  # Accepts 1 or more arguments
        help="Search terms (use 'tag:work' for tags)"
    )




    args = parser.parse_args()  # Only call parse_args() once!

    if args.command == "add":
        add_contact(args.first_name, args.last_name, args.email, args.phone)
    elif args.command == "list":
        list_contacts()
    elif args.command == "add-tag":
        add_tag_command(args.name)
    elif args.command == "assign-tag":
        assign_tag_command(args.contact_id, args.tag)
    elif args.command == "list-by-tag":
        list_by_tag_command(args.tag)
    elif args.command == "list-tags":
        list_tags_command()
    elif args.command == "remove-tag":
        remove_tag_command(args.contact_id, args.tag)
    elif args.command == "search":
        contacts = search_contacts(*args.query_terms)
        if contacts:
            print(f"Found {len(contacts)} matches for terms: {', '.join(args.query_terms)}")
            for contact in contacts:
                name = f"{contact[1]} {contact[2]}".strip()
                email = shorten(contact[3] or "", width=20)
                phone = contact[4] or ""
                print(f"{contact[0]:<5} {name:<30} {email:<20} {phone:<15}")
        else:
            print("No matches found.")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
