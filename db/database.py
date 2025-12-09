import sqlite3

# Create the table if it doesn't exist
def create_table():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, message TEXT, response TEXT)''')
    conn.commit()
    conn.close()

# Add a message to the database
def add_message(message, response):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO messages (message, response) VALUES (?, ?)''', (message, response))
    conn.commit()   
    conn.close()

# Get last messages from the database
def get_last_messages(limit: int=25):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM messages ORDER BY id DESC LIMIT ?''', (limit,))
    messages = cursor.fetchall()
    conn.close()
    return messages