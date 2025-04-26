# Email Client

This script implements an email client. It allows reading and sending emails from a Gmail account, as well as automatically replying to emails when the user is away.

## Requirements

* Python 3.10
* PyQt5
* configparser
* imaplib
* smtplib
* email

## Installation

1. Clone the repository:
    ```
    git clone https://github.com/Weisjan/Email-client.git
    ```

2. Fill in the `config.ini` file
    - email and password/token

## File Structure

```
Email-Client
├── config.ini
├── Client.py
└── Readme.md
```

| No | File Name | Details |
|----|-----------|---------|
| 1  | config.ini | Configuration file containing email account login details |
| 2  | Client.py | Main application script |
| 3  | Readme.md | Readme file |

## How It Works

The `Client.py` script is used to handle emails through a GUI created with PyQt5.

1. **Configuration**: The script reads the configuration from the `config.ini` file, which contains information about the Gmail account's email and password.
2. **User Interface**: A user interface is created with buttons for reading and sending emails, a text area for displaying emails, and a form for sending new messages.
3. **Reading Emails**: After clicking the "Read Emails" button, the application connects to Gmail’s IMAP server, fetches, and displays the 10 most recent emails. The user can filter emails by a keyword.
4. **Sending Emails**: After filling out the form and clicking the "Send Email" button, the application sends the message using Gmail’s SMTP server.
5. **Autoresponder**: If the user is inactive for more than 60 seconds, the application automatically replies to the most recently received email with an away message.

## Notes

- If connection errors occur during email reading or sending, the application will display appropriate error messages.
- The script automatically checks the user's last activity time and sends an autoresponder message in case of prolonged inactivity.

## Author

[Jan Weis](https://github.com/Weisjan)
