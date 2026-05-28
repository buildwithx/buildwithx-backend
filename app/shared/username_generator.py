import random
import string


class UsernameGenerator:
    CHARS = string.ascii_lowercase + string.digits

    @classmethod
    def generate(cls, length: int = 16) -> str:
        return "".join(random.choices(cls.CHARS, k=length))
