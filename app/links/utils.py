import random
import string

from loguru import logger

def generate_short_code(length: int = 8) -> str:
    logger.debug(f"Generating short code of length {length}")
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length)) 