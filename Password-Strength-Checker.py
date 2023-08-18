from zxcvbn import zxcvbn

class Wordlist:
    _cache = {}

    def __init__(self, file_path):
        self.file_path = file_path
        self.words = self.load_wordlist()

    def load_wordlist(self):
        if self.file_path in self._cache:
            return self._cache[self.file_path]

        try:
            with open(self.file_path, 'r') as file:
                wordlist = [line.strip() for line in file]
                self._cache[self.file_path] = wordlist
                return wordlist
        except FileNotFoundError:
            raise FileNotFoundError(f"Error: File '{self.file_path}' not found.")
        except Exception as e:
            raise Exception(f"Error loading wordlist from '{self.file_path}': {str(e)}")

    def is_word_in_list(self, word):
        return word in self.words


class StrengthResult:
    def __init__(self, strength: str, score: int, message: str):
        self.strength = strength
        self.score = score
        self.message = message


class PasswordStrength:
    def __init__(self, weak_wordlist_path: str = None, banned_wordlist_path: str = None):
        self.weak_wordlist = Wordlist(weak_wordlist_path) if weak_wordlist_path else None
        self.banned_wordlist = Wordlist(banned_wordlist_path) if banned_wordlist_path else None
        self.MIN_PASSWORD_LENGTH = 12

    def check_password_strength(self, password: str) -> StrengthResult:
        """
        Check the strength of a password.

        Args:
            password: The password to check.

        Returns:
            A StrengthResult object containing the password strength, score, and a message.
        """
        if len(password) < self.MIN_PASSWORD_LENGTH:
            return StrengthResult("Too short", 0, "Password should be at least 12 characters long.")

        if self.weak_wordlist and self.weak_wordlist.is_word_in_list(password):
            return StrengthResult("Weak", 0, "Password is commonly used and easily guessable.")

        password_strength = zxcvbn(password)
        score = password_strength["score"]

        if score < 3:
            suggestions = password_strength["feedback"]["suggestions"]
            return StrengthResult("Weak", score, f"Password is weak. Suggestions: {', '.join(suggestions)}")
        else:
            return StrengthResult("Strong", score, f"Password meets all the requirements. Score: {score}/4")

if __name__ == '__main__':
    while True:
        try:
            num_passwords = int(input("Enter the number of passwords to test (enter 0 to exit): "))
        except ValueError:
            print("Error: Invalid input. Please enter a valid number.")
            continue

        if num_passwords == 0:
            print("Exiting the tool.")
            break

        try:
            weak_wordlist_path = input("Enter the path to the weak wordlist file (leave blank for default): ")
            banned_wordlist_path = input("Enter the path to the banned wordlist file (leave blank for default): ")

            password_strength_checker = PasswordStrength(weak_wordlist_path, banned_wordlist_path)
        except Exception as e:
            print(f"Error initializing PasswordStrength: {str(e)}")
            continue

        for _ in range(num_passwords):
            password = input("Enter a password: ")
            result = password_strength_checker.check_password_strength(password)
            print(result.strength + ": " + result.message)

            if result.strength == "Weak":
                print("Suggested strong password:", password_strength_checker.generate_random_password())

    print("Thank you for using the Password Strength Checker.")

