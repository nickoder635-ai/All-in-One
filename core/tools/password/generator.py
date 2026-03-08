import string
import secrets

class PasswordGenerator:
    def __init__(self, lower=True, upper=True, numbers=True, symbols=False, no_repeat=False):
        self.lower = lower
        self.upper = upper
        self.numbers = numbers
        self.symbols = symbols
        self.no_repeat = no_repeat

    def generate(self, length=12):
        pool = ""
        if self.lower:
            pool += string.ascii_lowercase
        if self.upper:
            pool += string.ascii_uppercase
        if self.numbers:
            pool += string.digits
        if self.symbols:
            pool += string.punctuation

        if not pool:
            return ""

        if self.no_repeat:
            length = min(length, len(pool))
            pool_list = list(pool)
            for i in range(len(pool_list)-1, 0, -1):
                j = secrets.randbelow(i+1)
                pool_list[i], pool_list[j] = pool_list[j], pool_list[i]
            return ''.join(pool_list[:length])

        return ''.join(secrets.choice(pool) for _ in range(length))

    @staticmethod
    def calculate_strength(length, variety=0):
        # Strength بر اساس طول (main) + variety می‌تواند بعداً اضافه شود
        if length <= 3:
            return "Very Weak", "red"
        elif length <= 6:
            return "Weak", "orange"
        elif length <= 8:
            return "Good", "yellow"
        elif length <= 10:
            return "Strong", "green"
        else:
            return "Very Strong", "darkgreen"
