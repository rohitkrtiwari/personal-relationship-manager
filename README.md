# **🧠 Personal Relationship Manager (PRM)**

A command-line-based contact management system built to help you organize and maintain meaningful connections across email, social platforms, and phone. The project aims to unify contact data, enhance retrieval, and enable smart tagging & filtering.

    ⚠️ Project Status: Under Development (MVP Stage)

## **🚀 Vision**
The goal is to build a cross-platform, centralized contact intelligence tool that:
    
* Aggregates contacts from Email, LinkedIn, and Phone sources
* Allows intuitive tagging, searching, and categorization
* Supports CLI, GUI, and auto-overlay interfaces for quick access
* Enhances relationships with metadata like last contact time, channel, and notes

## **✅ Features Implemented (So Far)**
### **🧩 Core Components**

* SQLite3 database with schema for:
    * contacts: stores all people
    * tags: for contact grouping
    * contact_tags: many-to-many mapping

### **📥 Google Contacts Import**
* Imports .ods (OpenDocument Spreadsheet) exports from Google Contacts
* Cleans and deduplicates contact data
* Handles multiple phone numbers, photo URLs, etc.

    File: import_google_contacts.py

## **🖥️ CLI Functionality (cli.py)**
* Add contact manually via --first-name, --email, etc.
* Add/search/list tags
* Assign/unassign tags to contacts
* Multi-term smart search:

<code> python3 cli.py search "alice" "tag:work" </code>

## **🗂️ Database Schema**

contacts  
`id | first_name | last_name | email | phone | photo_url | source`

tags  
`id | name `

contact_tags  
`contact_id | tag_id`

## **🔧 How to Run**

* Install requirements  
`pip install pandas odfpy`

* Initialize database:  
`python database.py`

* Import Google Contacts:  
`python import_google_contacts.py`

* Use the CLI  
`python cli.py list`   
`python cli.py add --first-name  "Alice" --email "alice@example.com"`  
`python cli.py add-tag --name "friends"`  
`python cli.py assign-tag --contact-id 1 --tag "friends"`

## **🛠️ In Progress / TODO**

* LinkedIn contact integration
* Gmail-based relationship graph (via metadata)
* Phone contacts sync
* Tkinter overlay launcher (already partially working)
* Smart auto-tagging
* Notes & reminders

## **📂 Files Overview**

| File  | Purpose |
| ------------- | ------------- |
| database.py  | DB connection & schema setup  |
| cli.py  | Main CLI entrypoint  |
| import_google_contacts.py  | Imports .ods exports from Google Contacts  |
| prm.db  | The SQLite database file (generated)  |


## **📌 License & Contribution**
Currently a personal project — if you'd like to contribute or follow along, feel free to fork or reach out.