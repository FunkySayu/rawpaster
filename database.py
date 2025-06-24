import sqlite3
import os
import config

DATABASE_FILE = os.path.join(config.THIS_PATH, 'links.db')

def init_db():
    """Initializes the database and creates the links table if it doesn't exist."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS links (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fileid TEXT NOT NULL UNIQUE,
            user_key TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def add_link_to_db(fileid, user_key):
    """Adds a new link to the database."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO links (fileid, user_key) VALUES (?, ?)", (fileid, user_key))
        conn.commit()
    except sqlite3.IntegrityError:
        # Handle cases where fileid might already exist if generated non-uniquely, though unlikely with current generate_filename
        print(f"Error: Link with fileid {fileid} already exists.")
    finally:
        conn.close()

def get_all_links_from_db():
    """Retrieves all links from the database, ordered by timestamp descending."""
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row # Access columns by name
    cursor = conn.cursor()
    cursor.execute("SELECT fileid, user_key, timestamp FROM links ORDER BY timestamp DESC")
    links = cursor.fetchall()
    conn.close()
    return links
