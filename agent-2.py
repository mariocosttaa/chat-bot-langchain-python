# Standard library imports
import os
import time

# Third-party imports
from dotenv import load_dotenv

# LangChain imports
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.chat_history import InMemoryChatMessageHistory

# Google Gemini imports
from langchain_google_genai import ChatGoogleGenerativeAI

# Local imports
from logger import (
    setup_logger, log_session_start, log_session_end, log_user_input, 
    log_api_call_start, log_successful_response, log_error, log_debug,
    print_welcome_message, print_user_message, print_bot_message, 
    print_goodbye, print_thinking, print_typing_indicator
)
from tokens_counter import get_token_counts_with_cost
from helper import add_system_prompt_if_needed, format_error_message, handle_error

# Load environment variables
load_dotenv()

# Setup logger
logger = setup_logger('agent2')

# Initialize the Gemini Flash model
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.7
)

# Initialize memory (stores conversation history)
memory = InMemoryChatMessageHistory()

# System prompt - customize this to change the bot's behavior
SYSTEM_PROMPT = "You are a helpful and friendly assistant. Answer questions clearly and concisely."

# Main function
def main():
    log_session_start(logger)
    print_welcome_message("Chatbot with In-Memory")
    
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
            
            # Create HumanMessage object for user input
            user_message = HumanMessage(content=user_input)
            
            # Add user message to memory
            memory.add_message(user_message)
            
            # Get all messages from memory for context
            messages = memory.messages
            
            # Add system prompt at the beginning if needed
            messages = add_system_prompt_if_needed(messages, SYSTEM_PROMPT)
            
            log_debug(logger, f"Number of messages in context: {len(messages)}")
            
            # Show typing indicator
            print_typing_indicator()
            
            # Invoke LLM with conversation history
            log_api_call_start(logger)
            response = llm.invoke(messages)
            elapsed_time = time.time() - start_time
            
            # Get token counts and cost
            token_data = get_token_counts_with_cost(llm, messages, response)
            log_debug(logger, f"Token usage - Input: {token_data['input_tokens']}, Output: {token_data['output_tokens']}")
            log_debug(logger, f"Cost: {token_data['cost_formatted']}")
            
            # Create AIMessage object for bot response
            ai_message = AIMessage(content=response.content)
            
            # Add AI response to memory
            memory.add_message(ai_message)
            
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
