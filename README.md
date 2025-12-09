# 🤖 LangChain Chatbot with Gemini Flash

A feature-rich chatbot implementation using LangChain and Google's Gemini Flash model. This project includes two versions: one with persistent database storage and another with in-memory conversation history. Features include token counting, cost tracking, colored terminal UI, and comprehensive logging.

## 🎬 Preview

![Chatbot Demo](presentation.gif)

*Interactive terminal chatbot with colored UI, typing indicators, and real-time responses*

## 🛠️ Tech Stack

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google_Gemini-4285F4?style=for-the-badge&logo=google&logoColor=white)

**Technologies Used:**
- 🐍 **Python** - Programming language
- 🗄️ **SQLite** - Lightweight database for persistent storage
- ⛓️ **LangChain** - Framework for building LLM applications
- 🤖 **Google Gemini 2.5 Flash** - AI language model
- 📦 **python-dotenv** - Environment variable management

## ✨ Features

### Core Features
- 🤖 **Gemini Flash Integration**: Uses Google's Gemini 2.5 Flash model for fast and efficient responses
- 💬 **Conversation Memory**: Maintains conversation context during the session
- 💾 **Database Storage** (agent-1.py): Persistent conversation history stored in SQLite
- 🧠 **In-Memory Storage** (agent-2.py): Fast in-memory conversation history (resets on restart)
- ⚙️ **System Prompts**: Customizable system prompts to control bot behavior

### Advanced Features
- 🎨 **Colored Terminal UI**: Beautiful terminal interface with color-coded messages
  - 🔵 Blue for user messages
  - 🟢 Green for bot responses
  - 🟡 Yellow for thinking/typing indicators
  - 🔴 Red for error messages
  - Horizontal separator lines for visual clarity
- 📊 **Token Counting**: Automatic tracking of input and output tokens
- 💰 **Cost Calculation**: Real-time cost tracking based on token usage
  - Supports Gemini 2.5 Flash pricing ($0.075/1M input tokens, $0.30/1M output tokens)
  - Stores cost as float in database
  - Formatted currency display
- 📝 **Comprehensive Logging**: File-based logging system
  - All interactions logged to `logs/` folder
  - Separate log files per agent per day
  - Logs include: user input, API calls, responses, errors, timing
  - Debug information for troubleshooting
- 🗄️ **Enhanced Database Schema**:
  - Message and response storage
  - Token counts (input/output)
  - Cost tracking (float and formatted)
  - Agent type tracking (agent1/agent2)
  - Timestamp (created_at) for each message
  - Automatic database migration support
- 🛠️ **Helper Utilities**: Reusable utility functions for code organization
  - Database message conversion
  - Error handling and formatting
  - System prompt management

## 📋 Prerequisites

- 🐍 Python 3.8 or higher
- 🔑 Google API Key (get one from [Google AI Studio](https://aistudio.google.com/))

## 🚀 Installation

1. **Clone or navigate to the project directory:**
```bash
cd chat-bot-langchain-python
```

2. **Create a virtual environment:**
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Create a `.env` file in the project root:**
```env
GOOGLE_API_KEY=your_google_api_key_here
```

## 💻 Usage

**⚠️ Important:** Always activate the virtual environment before running the scripts!

```bash
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### Agent 1: Database-Persisted Chatbot 💾

This version stores conversation history in a SQLite database (`db/sqlite.db`), allowing conversations to persist across sessions.

```bash
python3 agent-1.py
```

**Features:**
- 🗄️ Stores up to 25 recent messages for context
- 💾 Conversation history persists in `db/sqlite.db`
- ⚙️ Automatically creates database table on first run
- 📊 Tracks tokens and costs for each interaction
- 🏷️ Tags messages with agent type and timestamp
- 🔄 Automatic database migration for schema updates

### Agent 2: In-Memory Chatbot 🧠

This version uses in-memory storage for faster performance, but conversation history is lost when the program exits.

```bash
python3 agent-2.py
```

**Features:**
- ⚡ Fast in-memory conversation history
- 🚫 No database dependencies
- 🔄 Conversation context maintained during session only
- 📊 Token counting and cost tracking (logged only)

## 📁 Project Structure

```
chat-bot-langchain-python/
├── agent-1.py              # Chatbot with database persistence
├── agent-2.py              # Chatbot with in-memory storage
├── helper.py               # Utility functions for code organization
├── logger.py               # Logging and terminal display functions
├── tokens_counter.py       # Token counting and cost calculation
├── db/
│   ├── database.py         # Database helper functions
│   └── sqlite.db           # SQLite database (auto-created)
├── logs/                   # Log files directory (auto-created)
│   └── chatbot_agent*.log  # Daily log files
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (create this)
└── README.md              # This file
```

## 📦 Dependencies

- `langchain` - ⛓️ LangChain framework for LLM applications
- `langchain-google-genai` - 🤖 Google Gemini integration
- `langchain-community` - 🔧 Additional LangChain features
- `python-dotenv` - 🔐 Environment variable management

## 🔄 How It Works

### Agent 1 (Database-Persisted)
1. **Initialization**: Creates/updates database table with all required columns
2. **Memory Management**: Retrieves last 25 messages from SQLite database for context
3. **Conversation Flow**: 
   - User input is received and logged
   - Previous messages are loaded from database
   - Full conversation history (with system prompt) is sent to LLM
   - Bot response is generated
   - Token counts and costs are calculated automatically
   - Message, response, tokens, cost, and timestamp are saved to database
   - Response is displayed with colored formatting

### Agent 2 (In-Memory)
1. **Initialization**: Creates in-memory conversation history
2. **Memory Management**: Maintains conversation in memory using `InMemoryChatMessageHistory`
3. **Conversation Flow**: 
   - User input is received and logged
   - Message is added to memory
   - Full conversation history (with system prompt) is sent to LLM
   - Bot response is generated
   - Token counts and costs are calculated and logged
   - Response is added to memory and displayed

## 🎨 Terminal UI Features

The chatbot features a beautiful colored terminal interface:

- **Welcome Message**: Formatted banner with agent name
- **User Messages**: Blue text with blue separator lines
- **Bot Messages**: Green text with green separator lines
- **Thinking Indicator**: Yellow "💭 Thinking..." message
- **Typing Animation**: Animated "🤖 Bot is typing..." indicator
- **Response Time**: Shows elapsed time for each response
- **Error Messages**: Red formatted error display
- **Goodbye Message**: Friendly farewell with formatting

## 📊 Token Counting & Cost Tracking

The system automatically tracks:
- **Input Tokens**: Number of tokens in the prompt
- **Output Tokens**: Number of tokens in the response
- **Cost**: Calculated based on Gemini 2.5 Flash pricing
  - Input: $0.075 per 1M tokens
  - Output: $0.30 per 1M tokens
- **Cost Formatting**: Displayed as currency string (e.g., "$0.000123")

All token and cost data is stored in the database (agent-1) and logged (both agents).

## 📝 Logging System

Comprehensive logging to file:
- **Location**: `logs/chatbot_agent1_YYYYMMDD.log` or `chatbot_agent2_YYYYMMDD.log`
- **Content**: 
  - Session start/end
  - User inputs
  - API call timing
  - Bot responses
  - Token usage
  - Cost information
  - Errors with full tracebacks
  - Debug information
- **Format**: Timestamp, log level, and message
- **Rotation**: New log file created each day

## 💬 Example Conversation

```
════════════════════════════════════════════════════════════
🤖 Chatbot with Database Memory is ready! Type 'exit' to quit.
════════════════════════════════════════════════════════════

👤 You: Hello, my name is Mario
────────────────────────────────────────────────────────────

💭 Thinking...
🤖 Bot is typing...

────────────────────────────────────────────────────────────
🤖 Bot: Hello Mario! Nice to meet you. How can I help you today?
   ⏱️  Response time: 0.85s
────────────────────────────────────────────────────────────

👤 You: What's my name?
────────────────────────────────────────────────────────────

💭 Thinking...
🤖 Bot is typing...

────────────────────────────────────────────────────────────
🤖 Bot: Your name is Mario!
   ⏱️  Response time: 0.72s
────────────────────────────────────────────────────────────

👤 You: exit
════════════════════════════════════════════════════════════
👋 Goodbye! Have a great day!
════════════════════════════════════════════════════════════
```

## 🔧 Configuration

### System Prompt
Customize the bot's behavior by editing the `SYSTEM_PROMPT` variable in `agent-1.py` or `agent-2.py`:

```python
SYSTEM_PROMPT = "You are a helpful and friendly assistant. Answer questions clearly and concisely."
```

### Memory Limit
For agent-1, adjust the number of messages to remember:

```python
max_remember_messages = 25  # Change this value
```

### Token Pricing
Update pricing constants in `tokens_counter.py` if using a different model:

```python
COST_PER_INPUT_TOKEN = 0.000000075  # $0.075 per 1M tokens
COST_PER_OUTPUT_TOKEN = 0.0000003   # $0.30 per 1M tokens
```

## 🔧 Troubleshooting

- **Import Errors**: Make sure you've activated the virtual environment and installed all dependencies
- **API Key Errors**: Verify your `GOOGLE_API_KEY` is correctly set in the `.env` file
- **Database Errors**: For agent-1.py, ensure you have write permissions in the project directory
- **API Quota Exceeded**: The free tier has a limit of 20 requests per day. Wait or upgrade your API plan
- **Colors Not Showing**: Some terminals may not support ANSI color codes. The functionality will still work without colors
- **Log Files Not Created**: Ensure the `logs/` directory has write permissions

## 📊 Database Schema

The `messages` table in `db/sqlite.db` contains:
- `id` - Primary key
- `message` - User input text
- `response` - Bot response text
- `input_tokens` - Number of input tokens (INTEGER)
- `output_tokens` - Number of output tokens (INTEGER)
- `cost` - Cost in dollars (REAL)
- `cost_formatted` - Formatted cost string (TEXT)
- `agent_type` - Which agent created the message (TEXT: 'agent1' or 'agent2')
- `created_at` - Timestamp in ISO format (TEXT)

## 🚀 Future Enhancements

Potential improvements:
- [ ] Web interface
- [ ] Multiple conversation threads
- [ ] Export conversation history
- [ ] Cost analytics dashboard
- [ ] Support for other LLM providers
- [ ] Conversation search functionality

## 📝 License

This is a simple educational project. Feel free to modify and use as needed.

---

Made with ❤️ using Python, SQLite, LangChain, and Google Gemini
