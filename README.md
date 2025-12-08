# LangChain Chatbot with Gemini Flash

A simple chatbot implementation using LangChain and Google's Gemini Flash model. This project includes two versions: one with in-memory conversation history and another with persistent database storage.

## Features

- 🤖 **Gemini Flash Integration**: Uses Google's Gemini 2.5 Flash model for fast and efficient responses
- 💬 **Conversation Memory**: Maintains conversation context during the session
- 💾 **Database Storage** (agent-1.py): Persistent conversation history stored in SQLite
- 🧠 **In-Memory Storage** (agent-2.py): Fast in-memory conversation history (resets on restart)

## Prerequisites

- Python 3.8+
- Google API Key (get one from [Google AI Studio](https://aistudio.google.com/))

## Installation

1. Clone or navigate to the project directory:
```bash
cd chat-bot-langchain-python
```

2. Create a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Copy the example environment file and edit it:
```bash
cp .env.example .env
# Then open .env and set your Google API key:
# GOOGLE_API_KEY=your_google_api_key_here
```

## Usage

### Agent 1: Database-Persisted Chatbot

This version stores conversation history in a SQLite database (`database.db`), allowing conversations to persist across sessions.

```bash
python3 agent-1.py
```

**Features:**
- Stores up to 25 recent messages for context
- Conversation history persists in `database.db`
- Automatically creates database table on first run

### Agent 2: In-Memory Chatbot

This version uses in-memory storage for faster performance, but conversation history is lost when the program exits.

```bash
python3 agent-2.py
```

**Features:**
- Fast in-memory conversation history
- No database dependencies
- Conversation context maintained during session only

## Project Structure

```
chat-bot-langchain-python/
├── agent-1.py          # Chatbot with database persistence
├── agent-2.py          # Chatbot with in-memory storage
├── database.py          # Database helper functions
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (create this)
└── README.md           # This file
```

## Dependencies

- `langchain` - LangChain framework
- `langchain-google-genai` - Google Gemini integration
- `langchain-community` - Additional LangChain features
- `python-dotenv` - Environment variable management

## How It Works

1. **Initialization**: The chatbot loads the Gemini Flash model with your API key
2. **Memory Management**: 
   - **agent-1.py**: Retrieves last 25 messages from database for context
   - **agent-2.py**: Maintains conversation in memory using `InMemoryChatMessageHistory`
3. **Conversation Flow**: 
   - User input is stored
   - Full conversation history is sent to the LLM
   - Bot response is generated and stored
   - Response is displayed to the user

## Example Conversation

```
🤖 Chatbot with memory is ready! Type 'exit' to quit.

You: Hello, my name is Mario
Bot: Hello Mario! Nice to meet you!

You: What's my name?
Bot: Your name is Mario!

You: exit
Goodbye!
```

## Troubleshooting

- **Import Errors**: Make sure you've activated the virtual environment and installed all dependencies
- **API Key Errors**: Verify your `GOOGLE_API_KEY` is correctly set in the `.env` file
- **Database Errors**: For agent-1.py, ensure you have write permissions in the project directory

## License

This is a simple educational project. Feel free to modify and use as needed.

