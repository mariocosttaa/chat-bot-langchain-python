# Standard library imports
import os

# Third-party imports
from dotenv import load_dotenv

# LangChain imports
from langchain_core.messages import HumanMessage, AIMessage

# Google Gemini imports
from langchain_google_genai import ChatGoogleGenerativeAI

from database import add_message, get_last_messages, create_table

# Create the table if it doesn't exist
create_table()

max_remember_messages = 25

# Load environment variables
load_dotenv()

# Initialize the Gemini Flash model
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.7
)

# Main function
def main():
    print("🤖 Chatbot with memory is ready! Type 'exit' to quit.\n")
    
    while True:
        user_input = input("You: ")
        
        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("Goodbye!")
            break
        
        try:
            # Get last messages from database for context
            messages = get_last_messages(max_remember_messages)
            
            # Convert database tuples to LangChain message format
            langchain_messages = []
            for msg_tuple in reversed(messages):  # Reverse to get chronological order
                msg_id, user_msg, bot_response = msg_tuple
                if user_msg:
                    langchain_messages.append(HumanMessage(content=user_msg))
                if bot_response:
                    langchain_messages.append(AIMessage(content=bot_response))
            
            # Add current user message
            langchain_messages.append(HumanMessage(content=user_input))
            
            # Invoke LLM with conversation history
            response = llm.invoke(langchain_messages)
            
            # Save both user message and bot response together
            add_message(user_input, response.content)
            
            print(f"\nBot: {response.content}\n")
        except Exception as e:
            print(f"Error: {str(e)}\n")

if __name__ == "__main__":
    main()
