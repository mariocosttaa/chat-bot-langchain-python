# Standard library imports
import logging
import os
import sys
import time
from datetime import datetime


def setup_logger(agent_name: str) -> logging.Logger:
    """
    Setup and configure logger for the chatbot agent.
    
    Args:
        agent_name: Name of the agent (e.g., 'agent1' or 'agent2')
    
    Returns:
        Configured logger instance
    """
    # Create logs directory if it doesn't exist
    logs_dir = "logs"
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    
    # Create log filename with date in logs folder
    log_filename = os.path.join(logs_dir, f"chatbot_{agent_name}_{datetime.now().strftime('%Y%m%d')}.log")
    
    # Configure logging (only to file, not terminal)
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename, encoding='utf-8')
        ],
        force=True  # Override any existing configuration
    )
    
    # Get logger instance
    logger = logging.getLogger(agent_name)
    logger.setLevel(logging.INFO)
    
    return logger


def log_session_start(logger: logging.Logger):
    """Log the start of a chatbot session."""
    logger.info("=" * 60)
    logger.info("Chatbot session started")
    logger.info("=" * 60)


def log_session_end(logger: logging.Logger):
    """Log the end of a chatbot session."""
    logger.info("User exited the chatbot")
    logger.info("=" * 60)


def log_user_input(logger: logging.Logger, user_input: str):
    """Log user input."""
    logger.info(f"User input: {user_input}")


def log_api_call_start(logger: logging.Logger):
    """Log the start of an API call."""
    logger.info("Calling LLM API...")


def log_successful_response(logger: logging.Logger, response: str, elapsed_time: float):
    """Log a successful API response."""
    logger.info(f"Bot response received in {elapsed_time:.2f} seconds")
    logger.info(f"Bot response: {response}")
    logger.info("-" * 60)


def log_error(logger: logging.Logger, error: Exception, elapsed_time: float):
    """Log an error with full details."""
    logger.error(f"Error occurred after {elapsed_time:.2f} seconds")
    logger.error(f"Error type: {type(error).__name__}")
    logger.error(f"Error message: {str(error)}")
    logger.error("Full traceback:", exc_info=True)
    logger.error("-" * 60)


def log_debug(logger: logging.Logger, message: str):
    """Log a debug message."""
    logger.debug(message)


# ANSI color codes for terminal
class Colors:
    """ANSI color codes for terminal output."""
    RESET = '\033[0m'
    BOLD = '\033[1m'
    
    # Text colors
    BLUE = '\033[94m'      # User messages
    GREEN = '\033[92m'     # Bot messages
    YELLOW = '\033[93m'    # Thinking/typing
    RED = '\033[91m'       # Errors
    CYAN = '\033[96m'      # Info/separators
    MAGENTA = '\033[95m'   # Welcome/goodbye
    
    # Background colors (optional)
    BG_BLUE = '\033[44m'
    BG_GREEN = '\033[42m'


def print_separator(color: str = Colors.CYAN):
    """Print a horizontal separator line."""
    print(f"{color}{'─' * 60}{Colors.RESET}")


# Terminal display functions for better chatbot experience
def print_welcome_message(agent_name: str = "Chatbot"):
    """Print a welcome message with nice formatting."""
    print(f"\n{Colors.MAGENTA}{Colors.BOLD}{'═' * 60}{Colors.RESET}")
    print(f"{Colors.MAGENTA}{Colors.BOLD}🤖 {agent_name} is ready! Type 'exit' to quit.{Colors.RESET}")
    print(f"{Colors.MAGENTA}{Colors.BOLD}{'═' * 60}{Colors.RESET}\n")


def print_thinking():
    """Show a thinking indicator."""
    print(f"{Colors.YELLOW}💭 Thinking...{Colors.RESET}", end="", flush=True)


def clear_thinking():
    """Clear the thinking indicator line."""
    print("\r" + " " * 30 + "\r", end="", flush=True)  # Clear line


def print_typing_indicator():
    """Show a typing indicator with animation."""
    for i in range(3):
        dots = "." * (i + 1)
        print(f"\r{Colors.YELLOW}🤖 Bot is typing{dots}   {Colors.RESET}", end="", flush=True)
        time.sleep(0.3)
    print("\r" + " " * 30 + "\r", end="", flush=True)  # Clear line


def print_user_message(message: str):
    """Print user message with nice formatting and color."""
    print_separator(Colors.BLUE)
    print(f"{Colors.BLUE}{Colors.BOLD}👤 You:{Colors.RESET} {Colors.BLUE}{message}{Colors.RESET}")
    print_separator(Colors.BLUE)
    print()


def print_bot_message(message: str, elapsed_time: float = None):
    """Print bot message with nice formatting, color, and separator."""
    print()  # Empty line before bot response
    print_separator(Colors.GREEN)
    print(f"{Colors.GREEN}{Colors.BOLD}🤖 Bot:{Colors.RESET} {Colors.GREEN}{message}{Colors.RESET}")
    if elapsed_time:
        print(f"{Colors.GREEN}   ⏱️  Response time: {elapsed_time:.2f}s{Colors.RESET}")
    print_separator(Colors.GREEN)
    print()  # Empty line after bot response


def print_goodbye():
    """Print a goodbye message."""
    print(f"\n{Colors.MAGENTA}{Colors.BOLD}{'═' * 60}{Colors.RESET}")
    print(f"{Colors.MAGENTA}{Colors.BOLD}👋 Goodbye! Have a great day!{Colors.RESET}")
    print(f"{Colors.MAGENTA}{Colors.BOLD}{'═' * 60}{Colors.RESET}\n")


def print_error_message(error_msg: str):
    """Print error message with formatting and color."""
    print(f"\n{Colors.RED}{Colors.BOLD}{'═' * 60}{Colors.RESET}")
    print(f"{Colors.RED}{Colors.BOLD}❌ Error: {error_msg}{Colors.RESET}")
    print(f"{Colors.RED}{Colors.BOLD}{'═' * 60}{Colors.RESET}")
    print(f"{Colors.RED}Chatbot closed due to error.{Colors.RESET}\n")

