import random
import string

def generate_short_code(length: int = 8) -> str:
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length)) 