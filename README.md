# Password Strength Checker

This is a Python script that allows you to check the strength of passwords and generate random passwords. It uses the zxcvbn library to evaluate the strength of passwords based on factors such as length, complexity, and common usage.

# Features

* Check the strength of a password and provide a score and feedback message.
* Option to use custom wordlists for checking weak and banned passwords.
* Simple command-line interface for easy interaction.

# Requirements

* Python 3.x
* zxcvbn library

# Usage

1. Clone the repository or download the script file:
```
git clone https://github.com/Sharma-IT/Password-Strength-Checker.git
cd Password-Strength-Checker
```

2. Install the zxcvbn library by running the following in your terminal:
```
pip install zxcvbn
```

3. Run the script using:
```
python password_strength_checker.py.
```

4. Follow the prompts to enter the number of passwords to test, the path to the weak wordlist file (optional), and the path to the banned wordlist file (optional).
Enter the passwords to test when prompted.

5. To exit the tool, enter 0 when prompted for the number of passwords to test.

Example:
```
$ python password_strength_checker.py
Enter the number of passwords to test (enter 0 to exit): 2
Enter the path to the weak wordlist file (leave blank for default):  
Enter the path to the banned wordlist file (leave blank for default):

Enter a password: password123
Too short: Password should be at least 12 characters long.
Suggested strong password: 8aB#2d$9f!Z

Enter a password: securePassword123!
Strong: Password meets all the requirements. Score: 4/4

Enter the number of passwords to test (enter 0 to exit): 0
Exiting the tool.
Thank you for using the Password Strength Checker.
```

# Contributing

Pull requests are welcomed. For major changes, please open an issue first to discuss what you would like to change.

# Contact

Shubham Sharma - [My LinkedIn](https://www.linkedin.com/in/sharma-it/) - shubhamsharma.emails@gmail.com.

# License

This project is licensed under the GPL 3.0 License - see the [LICENSE](LICENCE) file for details.
