# Standard library imports
from typing import List, Dict, Any

# LangChain imports
from langchain_core.messages import BaseMessage
from langchain_google_genai import ChatGoogleGenerativeAI

# Cost constants per token (in dollars)
# Gemini 2.5 Flash pricing: Input $0.075/1M tokens, Output $0.30/1M tokens
COST_PER_INPUT_TOKEN = 0.000000075  # $0.075 per 1M tokens
COST_PER_OUTPUT_TOKEN = 0.0000003   # $0.30 per 1M tokens


def count_tokens_from_response(response) -> Dict[str, int]:
    """
    Extract token counts from LLM response.
    
    Args:
        response: Response object from LLM invoke
    
    Returns:
        Dictionary with 'input_tokens' and 'output_tokens'
    """
    input_tokens = 0
    output_tokens = 0
    
    # Try to get token usage from response metadata
    if hasattr(response, 'response_metadata'):
        metadata = response.response_metadata
        if metadata:
            # Check for token usage in metadata
            if 'token_usage' in metadata:
                token_usage = metadata['token_usage']
                input_tokens = token_usage.get('prompt_tokens', 0)
                output_tokens = token_usage.get('completion_tokens', 0)
            # Alternative: check for usage_metadata (Gemini format)
            elif 'usage_metadata' in metadata:
                usage = metadata['usage_metadata']
                input_tokens = usage.get('prompt_token_count', 0)
                output_tokens = usage.get('candidates_token_count', 0)
    
    # Try to get from response object directly
    if hasattr(response, 'usage_metadata'):
        usage = response.usage_metadata
        input_tokens = getattr(usage, 'prompt_token_count', 0)
        output_tokens = getattr(usage, 'candidates_token_count', 0)
    
    return {
        'input_tokens': input_tokens,
        'output_tokens': output_tokens
    }


def estimate_tokens_from_messages(messages: List[BaseMessage], model: str = "gemini-2.5-flash") -> int:
    """
    Estimate token count from messages (fallback if API doesn't provide).
    
    Args:
        messages: List of message objects
        model: Model name for estimation
    
    Returns:
        Estimated token count
    """
    # Simple estimation: ~4 characters per token for English text
    total_chars = 0
    for msg in messages:
        if hasattr(msg, 'content'):
            content = str(msg.content)
            total_chars += len(content)
    
    # Rough estimation: 1 token ≈ 4 characters
    estimated_tokens = total_chars // 4
    return estimated_tokens


def get_token_counts(llm: ChatGoogleGenerativeAI, messages: List[BaseMessage], response) -> Dict[str, int]:
    """
    Get token counts from response, with fallback estimation.
    
    Args:
        llm: The LLM instance
        messages: Input messages
        response: Response from LLM
    
    Returns:
        Dictionary with 'input_tokens' and 'output_tokens'
    """
    # Try to get actual token counts from response
    token_counts = count_tokens_from_response(response)
    
    # If no tokens found, use estimation
    if token_counts['input_tokens'] == 0:
        token_counts['input_tokens'] = estimate_tokens_from_messages(messages)
    
    if token_counts['output_tokens'] == 0 and hasattr(response, 'content'):
        # Estimate output tokens
        output_text = str(response.content)
        token_counts['output_tokens'] = len(output_text) // 4
    
    return token_counts


def calculate_cost(input_tokens: int, output_tokens: int) -> Dict[str, Any]:
    """
    Calculate cost based on token counts.
    
    Args:
        input_tokens: Number of input tokens
        output_tokens: Number of output tokens
    
    Returns:
        Dictionary with 'cost' (FLOAT in dollars) and 'cost_formatted' (currency string)
    """
    # Calculate total cost in dollars
    total_cost_dollars = (input_tokens * COST_PER_INPUT_TOKEN) + (output_tokens * COST_PER_OUTPUT_TOKEN)
    
    # Format as currency string
    cost_formatted = f"${total_cost_dollars:.6f}"
    
    return {
        'cost': total_cost_dollars,
        'cost_formatted': cost_formatted
    }


def get_token_counts_with_cost(llm: ChatGoogleGenerativeAI, messages: List[BaseMessage], response) -> Dict[str, Any]:
    """
    Get token counts and calculate cost.
    
    Args:
        llm: The LLM instance
        messages: Input messages
        response: Response from LLM
    
    Returns:
        Dictionary with 'input_tokens', 'output_tokens', 'cost', and 'cost_formatted'
    """
    # Get token counts
    token_counts = get_token_counts(llm, messages, response)
    
    # Calculate cost
    cost_info = calculate_cost(token_counts['input_tokens'], token_counts['output_tokens'])
    
    # Combine results
    return {
        'input_tokens': token_counts['input_tokens'],
        'output_tokens': token_counts['output_tokens'],
        'cost': cost_info['cost'],
        'cost_formatted': cost_info['cost_formatted']
    }

