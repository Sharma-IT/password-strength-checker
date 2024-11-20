# Password Strength Checker

A comprehensive password strength checking tool with both GUI and CLI interfaces. This application helps users create and validate secure passwords using advanced strength checking algorithms.

## Features

- **Dual Interface**: Choose between a user-friendly GUI or efficient CLI
- **Password Strength Analysis**: Uses the `zxcvbn` algorithm for realistic password strength assessment
- **Password Generation**: Create strong, random passwords of customisable length
- **Comprehensive Checks**:
  - Minimum length requirements
  - Character complexity (uppercase, lowercase, numbers, special characters)
  - Common password detection
  - Banned password detection
- **Improvement Suggestions**: Get specific recommendations to strengthen weak passwords
- **Export Functionality**: Save password check results to JSON (GUI mode)
- **Logging**: Track password checks with detailed logs

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/password-strength-checker.git
cd password-strength-checker
```

2. Install dependencies:
```bash
pip install zxcvbn
```

3. Ensure you have the required wordlist files:
- `weak_passwords.txt`: List of commonly used weak passwords
- `banned_passwords.txt`: List of banned passwords

## Usage

### GUI Mode

Run without arguments to launch the graphical interface:
```bash
python password_strength_checker.py
```

### CLI Mode

1. Interactive CLI:
```bash
python password_strength_checker.py --cli
```

2. Direct password check:
```bash
python password_strength_checker.py --check "your_password_here"
```

3. Generate password:
```bash
# Default length (16 characters)
python password_strength_checker.py --generate

# Custom length
python password_strength_checker.py --generate --length 20
```

### Command Line Arguments

- `--cli`: Launch interactive CLI mode
- `--check PASSWORD`: Check strength of a specific password
- `--generate`: Generate a strong password
- `--length N`: Specify length for generated password (default: 16)

## Features in Detail

### Password Strength Criteria

- Minimum length: 12 characters
- Character complexity:
  - Uppercase letters
  - Lowercase letters
  - Numbers
  - Special characters
- Checks against common weak passwords
- Checks against banned passwords
- Uses zxcvbn for advanced pattern matching

### GUI Features

- Password strength visualisation
- Password generation with clipboard support
- Export results to JSON
- Security tips display
- Interactive feedback

### CLI Features

- Interactive menu-driven interface
- Direct command execution
- Password generation with customisable length
- Detailed strength analysis output

## Logging

The application logs all password checks to `password_checker.log` with the following information:
- Timestamp
- Action performed
- Strength result

## Security Notes

- Passwords are never stored permanently
- All processing is done locally
- No external API calls for password checking
- Secure random generation for new passwords

## Dependencies

- Python 3.x
- tkinter (included in standard Python distribution)
- zxcvbn

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## License

This project is licensed under the GPL 3.0 License - see the [LICENSE](LICENSE) file for details.
