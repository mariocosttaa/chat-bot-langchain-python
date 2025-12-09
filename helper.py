# Standard library imports
from typing import List, Tuple

# LangChain imports
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage


def convert_db_messages_to_langchain(db_messages: List[Tuple], system_prompt: str = None) -> List:
    """
    Convert database message tuples to LangChain message format.
    
    Args:
        db_messages: List of tuples from database (id, message, response, ...)
        system_prompt: Optional system prompt to add at the beginning
    
    Returns:
        List of LangChain message objects
    """
    langchain_messages = []
    
    # Convert database tuples to LangChain message format
    # Database columns: id, message, response, input_tokens, output_tokens, cost, cost_formatted, agent_type, created_at
    for msg_tuple in reversed(db_messages):  # Reverse to get chronological order
        user_msg = msg_tuple[1]  # message column
        bot_response = msg_tuple[2]  # response column
        
        if user_msg:
            langchain_messages.append(HumanMessage(content=user_msg))
        if bot_response:
            langchain_messages.append(AIMessage(content=bot_response))
    
    # Add system prompt at the beginning if provided
    if system_prompt:
        langchain_messages = [SystemMessage(content=system_prompt)] + langchain_messages
    
    return langchain_messages


def format_error_message(error: Exception) -> str:
    """
    Format error message for user display.
    
    Args:
        error: Exception object
    
    Returns:
        Simple error message string
    """
    error_title = type(error).__name__
    error_message = str(error)
    
    # Extract simple error message
    if "RESOURCE_EXHAUSTED" in error_message or "429" in error_message:
        return "API Quota Exceeded"
    elif "API" in error_title or "Error" in error_title:
        return error_title.replace("Error", "").strip()
    else:
        return error_title


def handle_error(error: Exception, logger, elapsed_time: float) -> bool:
    """
    Handle error: log it and return True if chat should close.
    
    Args:
        error: Exception object
        logger: Logger instance
        elapsed_time: Time elapsed before error
    
    Returns:
        True if chat should close, False otherwise
    """
    from logger import log_error, print_error_message
    
    log_error(logger, error, elapsed_time)
    
    simple_error = format_error_message(error)
    print_error_message(simple_error)
    
    return True  # Close chat on error


def add_system_prompt_if_needed(messages: List, system_prompt: str) -> List:
    """
    Add system prompt to messages if not already present.
    
    Args:
        messages: List of LangChain messages
        system_prompt: System prompt text
    
    Returns:
        List of messages with system prompt at the beginning
    """
    if not messages or not isinstance(messages[0], SystemMessage):
        return [SystemMessage(content=system_prompt)] + messages
    return messages

