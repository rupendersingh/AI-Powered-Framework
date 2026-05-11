import time
from functools import wraps
from app.logger import get_logger

logger = get_logger("ai_qa")

def retry(retries=3, delay=2):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, retries+1):
                try:
                    logger.info(
                        f"Executing function | attempt={attempt}"
                    )
                    return func(*args, **kwargs)
                except Exception as error:
                    logger.warning(
                        f"Attempt failed | "
                        f"attempt={attempt} | "
                        f"error={str(error)}"
                    )
                     
                    # Final attempt failed
                    if (attempt == retries):
                        logger.error(
                            f"All retry attempts failed | "
                            f"function = {func.__name__}"
                        )
                        raise

                    logger.info(
                        f"Retrying after delay | delay={delay}s"
                    )

                    time.sleep(delay)
        return wrapper
    return decorator
