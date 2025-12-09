# Standard library imports
import logging
from datetime import datetime


def setup_logger(agent_name: str) -> logging.Logger:
    """
    Setup and configure logger for the chatbot agent.
    
    Args:
        agent_name: Name of the agent (e.g., 'agent1' or 'agent2')
    
    Returns:
        Configured logger instance
    """
    # Create log filename with date
    log_filename = f"chatbot_{agent_name}_{datetime.now().strftime('%Y%m%d')}.log"
    
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

