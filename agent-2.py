# Standard library imports
import os

# Third-party imports
from dotenv import load_dotenv

# LangChain imports
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.chat_history import InMemoryChatMessageHistory

# Google Gemini imports
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables
load_dotenv()

# Initialize the Gemini Flash model
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.7
)

# Initialize memory (stores conversation history)
memory = InMemoryChatMessageHistory()

# Main function
def main():
    print("🤖 Chatbot with memory is ready! Type 'exit' to quit.\n")
    
    while True:
        user_input = input("You: ")
        
        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("Goodbye!")
            break
        
        try:
            # Create HumanMessage object for user input
            user_message = HumanMessage(content=user_input)
            
            # Add user message to memory
            memory.add_message(user_message)
            
            # Get all messages from memory for context
            messages = memory.messages
            
            # Invoke LLM with conversation history
            response = llm.invoke(messages)
            
            # Create AIMessage object for bot response
            ai_message = AIMessage(content=response.content)
            
            # Add AI response to memory
            memory.add_message(ai_message)
            
            print(f"\nBot: {response.content}\n")
        except Exception as e:
            print(f"Error: {str(e)}\n")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    main()
