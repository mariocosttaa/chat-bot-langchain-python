# Standard library imports
import os
import time

# Third-party imports
from dotenv import load_dotenv

# LangChain imports
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# Google Gemini imports
from langchain_google_genai import ChatGoogleGenerativeAI

# Local imports
from db.database import add_message, get_last_messages, create_table
from logger import (
    setup_logger, log_session_start, log_session_end, log_user_input, 
    log_api_call_start, log_successful_response, log_error, log_debug,
    print_welcome_message, print_user_message, print_bot_message, 
    print_goodbye, print_thinking, print_typing_indicator
)
from helper import convert_db_messages_to_langchain, format_error_message, handle_error

# Initialize database - create/update table if it doesn't exist
create_table()

max_remember_messages = 25

# Load environment variables
load_dotenv()

# Setup logger
logger = setup_logger('agent1')

# Initialize the Gemini Flash model
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.7
)

# System prompt - customize this to change the bot's behavior
SYSTEM_PROMPT = "You are a helpful and friendly assistant. Answer questions clearly and concisely."

# Main function
def main():
    log_session_start(logger)
    print_welcome_message("Chatbot with Database Memory")
    
    while True:
        from logger import Colors, print_separator
        user_input = input(f"{Colors.BLUE}👤 You: {Colors.RESET}").strip()
        
        if not user_input:
            continue
        
        if user_input.lower() in ['exit', 'quit', 'bye']:
            log_session_end(logger)
            print_goodbye()
            break
        
        # Print separator line after user input
        print_separator(Colors.BLUE)
        print()  # Empty line after separator
        
        # Log user input
        log_user_input(logger, user_input)
        start_time = time.time()
        
        try:
            # Show thinking indicator
            print_thinking()
            
            # Get last messages from database for context
            log_debug(logger, "Retrieving messages from database...")
            db_messages = get_last_messages(max_remember_messages)
            log_debug(logger, f"Retrieved {len(db_messages)} messages from database")
            
            # Convert database messages to LangChain format (without system prompt)
            langchain_messages = convert_db_messages_to_langchain(db_messages)
            
            # Add current user message
            langchain_messages.append(HumanMessage(content=user_input))
            
            # Add system prompt at the beginning
            langchain_messages = [SystemMessage(content=SYSTEM_PROMPT)] + langchain_messages
            
            log_debug(logger, f"Total messages for context: {len(langchain_messages)}")
            
            # Show typing indicator
            print_typing_indicator()
            
            # Invoke LLM with conversation history
            log_api_call_start(logger)
            response = llm.invoke(langchain_messages)
            elapsed_time = time.time() - start_time
            
            # Save message to database (function handles tokens, cost, datetime, and agent_type)
            log_debug(logger, "Saving messages to database...")
            add_message(
                message=user_input,
                response_text=response.content,
                agent_type='agent1',
                llm=llm,
                messages=langchain_messages,
                response_obj=response
            )
            
            # Log successful response
            log_successful_response(logger, response.content, elapsed_time)
            
            # Print bot response with nice formatting
            print_bot_message(response.content, elapsed_time)
        except Exception as e:
            elapsed_time = time.time() - start_time
            if handle_error(e, logger, elapsed_time):
                break

if __name__ == "__main__":
    main()
