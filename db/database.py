import sqlite3
from datetime import datetime
from typing import Optional, List

DATABASE_PATH = 'db/sqlite.db'

# Create the table if it doesn't exist
def create_table():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            message TEXT, 
            response TEXT,
            input_tokens INTEGER DEFAULT 0,
            output_tokens INTEGER DEFAULT 0,
            cost REAL DEFAULT 0.0,
            cost_formatted TEXT DEFAULT '$0.000000',
            agent_type TEXT DEFAULT 'agent1',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    # Add new columns if table exists without them (migration)
    try:
        cursor.execute('ALTER TABLE messages ADD COLUMN input_tokens INTEGER DEFAULT 0')
    except sqlite3.OperationalError:
        pass  # Column already exists
    try:
        cursor.execute('ALTER TABLE messages ADD COLUMN output_tokens INTEGER DEFAULT 0')
    except sqlite3.OperationalError:
        pass  # Column already exists
    try:
        cursor.execute('ALTER TABLE messages ADD COLUMN cost REAL DEFAULT 0.0')
    except sqlite3.OperationalError:
        pass  # Column already exists
    try:
        cursor.execute('ALTER TABLE messages ADD COLUMN cost_formatted TEXT DEFAULT \'$0.000000\'')
    except sqlite3.OperationalError:
        pass  # Column already exists
    try:
        cursor.execute('ALTER TABLE messages ADD COLUMN agent_type TEXT DEFAULT \'agent1\'')
    except sqlite3.OperationalError:
        pass  # Column already exists
    try:
        cursor.execute('ALTER TABLE messages ADD COLUMN created_at TEXT DEFAULT CURRENT_TIMESTAMP')
    except sqlite3.OperationalError:
        pass  # Column already exists
    conn.commit()
    conn.close()

# Add a message to the database
def add_message(message: str, response_text: str, agent_type: str = 'agent1', 
                llm=None, messages: Optional[List] = None, response_obj=None):
    """
    Add a message to the database with automatic token, cost, and datetime calculation.
    
    Args:
        message: User message text (input)
        response_text: Bot response text (output)
        agent_type: Type of agent ('agent1' or 'agent2'), defaults to 'agent1'
        llm: LLM instance (optional, for token calculation)
        messages: List of messages sent to LLM (optional, for token calculation)
        response_obj: Response object from LLM (optional, for token calculation)
    
    The function automatically handles:
    - Datetime (created_at) - set to current time
    - Token counting (if llm, messages, and response_obj are provided)
    - Cost calculation (if tokens are calculated)
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Get current datetime in ISO format (handled automatically)
    current_datetime = datetime.now().isoformat()
    
    # Calculate tokens and cost if LLM and response are provided (handled automatically)
    input_tokens = 0
    output_tokens = 0
    cost = 0.0
    cost_formatted = '$0.000000'
    
    if llm and messages and response_obj:
        try:
            from tokens_counter import get_token_counts_with_cost
            token_data = get_token_counts_with_cost(llm, messages, response_obj)
            input_tokens = token_data['input_tokens']
            output_tokens = token_data['output_tokens']
            cost = token_data['cost']
            cost_formatted = token_data['cost_formatted']
        except Exception:
            # If token calculation fails, use defaults
            pass
    
    cursor.execute('''
        INSERT INTO messages (message, response, input_tokens, output_tokens, cost, cost_formatted, agent_type, created_at) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (message, response_text, input_tokens, output_tokens, cost, cost_formatted, agent_type, current_datetime))
    conn.commit()   
    conn.close()

# Get last messages from the database
def get_last_messages(limit: int=25):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM messages ORDER BY id DESC LIMIT ?''', (limit,))
    messages = cursor.fetchall()
    conn.close()
    return messages