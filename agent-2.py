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
from logger import setup_logger, log_session_start, log_session_end, log_user_input, log_api_call_start, log_successful_response, log_error, log_debug

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
    print("🤖 Chatbot with memory is ready! Type 'exit' to quit.\n")
    
    while True:
        user_input = input("You: ")
        
        if user_input.lower() in ['exit', 'quit', 'bye']:
            log_session_end(logger)
            print("Goodbye!")
            break
        
        # Log user input
        log_user_input(logger, user_input)
        start_time = time.time()
        
        try:
            # Create HumanMessage object for user input
            user_message = HumanMessage(content=user_input)
            
            # Add user message to memory
            memory.add_message(user_message)
            
            # Get all messages from memory for context
            messages = memory.messages
            
            # Add system prompt at the beginning (only if not already present)
            if not messages or not isinstance(messages[0], SystemMessage):
                messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages
            
            log_debug(logger, f"Number of messages in context: {len(messages)}")
            
            # Invoke LLM with conversation history
            log_api_call_start(logger)
            response = llm.invoke(messages)
            elapsed_time = time.time() - start_time
            
            # Create AIMessage object for bot response
            ai_message = AIMessage(content=response.content)
            
            # Add AI response to memory
            memory.add_message(ai_message)
            
            # Log successful response
            log_successful_response(logger, response.content, elapsed_time)
            
            print(f"\nBot: {response.content}\n")
        except Exception as e:
            elapsed_time = time.time() - start_time
            log_error(logger, e, elapsed_time)
            
            # Get error title/type
            error_title = type(e).__name__
            error_message = str(e)
            
            # Extract simple error message (first line or key part)
            if "RESOURCE_EXHAUSTED" in error_message or "429" in error_message:
                simple_error = "API Quota Exceeded"
            elif "API" in error_title or "Error" in error_title:
                simple_error = error_title.replace("Error", "").strip()
            else:
                simple_error = error_title
            
            print(f"\n❌ Error: {simple_error}\n")
            print("Chatbot closed due to error.\n")
            break

if __name__ == "__main__":
    main()
