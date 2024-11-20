"""A GUI and CLI application for checking and generating secure passwords.

This module provides functionality to:
- Check password strength using various criteria
- Generate secure random passwords
- Suggest improvements for weak passwords
- Export password check results
Supports both GUI and CLI interfaces
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import re
import random
import string
import logging
import json
import argparse
import sys
from functools import lru_cache

from zxcvbn import zxcvbn

logging.basicConfig(filename='password_checker.log', level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s')

class Wordlist:
    """Class to handle wordlists for password checking."""

    _cache = {}

    def __init__(self, file_path):
        self.file_path = file_path
        self.words = self.load_wordlist()

    def load_wordlist(self):
        """Load wordlist from file."""
        if self.file_path in self._cache:
            return self._cache[self.file_path]

        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                wordlist = [line.strip() for line in file]
                self._cache[self.file_path] = wordlist
                return wordlist
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Error: File '{self.file_path}' not found.") from e
        except Exception as e:
            raise RuntimeError(
                f"Error loading wordlist from '{self.file_path}': {str(e)}"
            ) from e

    def is_word_in_list(self, word):
        """Check if a word is in the wordlist."""
        return word in self.words

# pylint: disable=R0903
class StrengthResult:
    """Class to store password strength check results."""

    def __init__(self, strength: str, score: int, message: str):
        self.strength = strength
        self.score = score
        self.message = message

class PasswordStrength:
    """Class to handle password strength checking and related operations."""

    def __init__(self, weak_wordlist_path: str = "./weak_passwords.txt",
        banned_wordlist_path: str = "./banned_passwords.txt"):
        self.weak_wordlist = (Wordlist(weak_wordlist_path)
            if weak_wordlist_path else None)
        self.banned_wordlist = (Wordlist(banned_wordlist_path)
            if banned_wordlist_path else None)
        self.min_password_length = 12
        self.strength_mapping = {
            0: "Very Weak",
            1: "Weak",
            2: "Moderate",
            3: "Strong",
            4: "Very Strong"
        }

    @lru_cache(maxsize=1000)
    def check_password_strength(self, password: str) -> StrengthResult:
        """Check the strength of a given password."""
        if len(password) < self.min_password_length:
            return StrengthResult("Too short", 0, "Password should be at least 12 characters long.")

        if self.weak_wordlist and self.weak_wordlist.is_word_in_list(password):
            return StrengthResult("Weak", 0, "Password is commonly used and easily guessable.")

        if self.banned_wordlist and self.banned_wordlist.is_word_in_list(password):
            return StrengthResult("Banned", 0,
                "This password is not allowed, as it is commonly found in data leaks.")

        password_strength = zxcvbn(password)
        score = password_strength["score"]
        strength = self.strength_mapping[score]
        complexity_issues = []
        if not re.search(r'[A-Z]', password):
            complexity_issues.append("uppercase letter")
        if not re.search(r'[a-z]', password):
            complexity_issues.append("lowercase letter")
        if not re.search(r'\d', password):
            complexity_issues.append("number")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            complexity_issues.append("special character")

        if complexity_issues:
            return StrengthResult("Weak", score,
                f"Password lacks complexity. Missing: {', '.join(complexity_issues)}.")

        if score >= 3:
            return StrengthResult(strength, score,
                f"Password meets all the requirements. Score: {score}/4")

        suggestions = password_strength["feedback"]["suggestions"]
        return StrengthResult(strength, score,
            f"Password is {strength.lower()}. Suggestions: {', '.join(suggestions)}")

    def generate_random_password(self, length=16):
        """Generate a random password."""
        characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(characters) for _ in range(length))

    def suggest_improvements(self, password: str) -> str:
        """Suggest improvements for a given password."""
        result = self.check_password_strength(password)
        suggestions = []

        if len(password) < self.min_password_length:
            suggestions.append(f"Increase length to at least {self.min_password_length} characters")

        if not re.search(r'[A-Z]', password):
            suggestions.append("Add uppercase letters")
        if not re.search(r'[a-z]', password):
            suggestions.append("Add lowercase letters")
        if not re.search(r'\d', password):
            suggestions.append("Add numbers")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            suggestions.append("Add special characters")

        if not suggestions:
            suggestions = result.message.split("Suggestions: ")[-1].split(", ")

        return "Suggested improvements:\n\n" + "\n".join(f"- {s}" for s in suggestions)

# pylint: disable=R0902
class PasswordStrengthGUI:
    """GUI class for Password Strength Checker."""

    def __init__(self, master):
        self.master = master
        master.title("Password Strength Checker")

        self.password_strength = PasswordStrength()

        self.label = tk.Label(master, text="Enter password:")
        self.label.pack()

        self.password_entry = tk.Entry(master, show="*")
        self.password_entry.pack()
        self.password_entry.bind('<Return>', lambda event: self.check_password())

        self.check_button = tk.Button(master, text="Check Strength", command=self.check_password)
        self.check_button.pack()
        self.result_label = tk.Label(master, text="")
        self.result_label.pack()

        self.suggestion_label = tk.Label(master, text="")
        self.suggestion_label.pack()

        self.generate_button = tk.Button(master, text="Generate Strong Password",
            command=self.generate_password)
        self.generate_button.pack()

        self.export_button = tk.Button(master, text="Export Results", command=self.export_results)
        self.export_button.pack()

        self.quit_button = tk.Button(master, text="Quit", command=master.quit)
        self.quit_button.pack()

        self.tip_label = tk.Label(master, text="\nTips:\n"
            "\n• Do not include any personal information in your password"
            "\n• Use a combination of uppercase and lowercase letters"
            "\n• Include numbers and special characters"
            "\n• Avoid common words or phrases"
            "\n• Use a unique password for each account",
            fg="light blue", justify="left")
        self.tip_label.pack()

        # Added text box to display generated password
        self.password_display = tk.Text(master, height=2, width=30, wrap=tk.WORD)
        self.password_display.pack()

        # Added Copy to Clipboard Button
        self.copy_button = tk.Button(master, text="Copy to Clipboard", command=self.copy_password)
        self.copy_button.pack()

        self.results = []

    def check_password(self):
        """Check the strength of the entered password."""
        password = self.password_entry.get()
        result = self.password_strength.check_password_strength(password)
        self.result_label.config(text=f"{result.strength}: {result.message}")
        suggestions = self.password_strength.suggest_improvements(password)
        self.suggestion_label.config(text=suggestions)
        self.results.append({"password": password, "strength": result.strength,
        "message": result.message})
        logging.info("Password checked: %s", result.strength)

    def generate_password(self):
        """Generate a random strong password."""
        password = self.password_strength.generate_random_password()
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)
        # Insert the generated password into the text box
        self.password_display.delete(1.0, tk.END)
        self.password_display.insert(tk.END, password)
        copy_to_clipboard = messagebox.askyesno("Generated Password",
            f"Generated password: {password}\n\nDo you want to copy the password to clipboard?")
        if copy_to_clipboard:
            self.master.clipboard_clear()
            self.master.clipboard_append(password)
            messagebox.showinfo("Clipboard", "Password copied to clipboard.")

    def copy_password(self):
        """Copy the password from the text box to clipboard."""
        password = self.password_display.get(1.0, tk.END).strip()
        self.master.clipboard_clear()
        self.master.clipboard_append(password)
        messagebox.showinfo("Clipboard", "Password copied to clipboard.")

    def export_results(self):
        """Export the password check results to a JSON file."""
        if not self.results:
            messagebox.showerror("Error", "No results to export.")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
        if not file_path:
            return
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(self.results, file, indent=4)
        messagebox.showinfo("Export Successful", f"Results exported to {file_path}.")

class PasswordStrengthCLI:
    """CLI interface for Password Strength Checker."""

    def __init__(self):
        self.password_strength = PasswordStrength()

    def check_password(self, password):
        """Check password strength and print results."""
        result = self.password_strength.check_password_strength(password)
        print(f"\nStrength: {result.strength}")
        print(f"Message: {result.message}")
        print(self.password_strength.suggest_improvements(password))

    def generate_password(self, length=16):
        """Generate and display a random password."""
        password = self.password_strength.generate_random_password(length)
        print(f"\nGenerated Password: {password}")
        self.check_password(password)
        return password

def main():
    """Main entry point for both GUI and CLI interfaces."""
    parser = argparse.ArgumentParser(description="Password Strength Checker")
    parser.add_argument("--cli", action="store_true", help="Run in CLI mode")
    parser.add_argument("--check", type=str, help="Check strength of provided password")
    parser.add_argument("--generate", action="store_true", help="Generate a strong password")
    parser.add_argument("--length", type=int, default=16, help="Length of generated password")

    args = parser.parse_args()

    if args.cli or args.check or args.generate:
        cli = PasswordStrengthCLI()
        if args.check:
            cli.check_password(args.check)
        elif args.generate:
            cli.generate_password(args.length)
        elif args.cli:
            while True:
                print("\nPassword Strength Checker CLI")
                print("1. Check Password Strength")
                print("2. Generate Strong Password")
                print("3. Exit")
                choice = input("\nEnter your choice (1-3): ")

                if choice == "1":
                    password = input("Enter password to check: ")
                    cli.check_password(password)
                elif choice == "2":
                    length = input("Enter desired password length (default 16): ")
                    try:
                        length = int(length) if length else 16
                        cli.generate_password(length)
                    except ValueError:
                        print("Invalid length. Using default length of 16.")
                        cli.generate_password()
                elif choice == "3":
                    print("Goodbye!")
                    sys.exit(0)
                else:
                    print("Invalid choice. Please try again.")
    else:
        root = tk.Tk()
        PasswordStrengthGUI(root)
        root.mainloop()

if __name__ == "__main__":
    main()
