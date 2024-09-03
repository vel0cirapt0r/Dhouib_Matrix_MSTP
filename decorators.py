import time
import logging
from functools import wraps

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Decorator for measuring the time
def measure_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        log_message = f"Execution time for {func.__name__}: {execution_time:.6f} seconds"

        # ANSI escape codes for color
        color_start = "\033[1;32m"  # Green color
        color_end = "\033[0m"  # Reset color

        # Log message with color
        colored_log_message = f"{color_start}{log_message}{color_end}"

        logger.info(colored_log_message)
        return result

    return wrapper


# Decorator for handling errors
def handle_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            # ANSI escape codes for color
            color_start = "\033[1;31m"  # Red color
            color_end = "\033[0m"  # Reset color

            # Error message with color
            colored_error_message = f"{color_start}Error in {func.__name__}: {str(e)}{color_end}"

            logger.error(colored_error_message)
            return None

    return wrapper

