# Email Client README

## Description
This is a simple email client application built using Python's Tkinter library for the GUI, and the `smtplib` and `imaplib` modules for sending and receiving emails respectively. It allows users to send, receive, and delete emails from their email account.

## Features
- **Send Email:** Users can compose and send emails to recipients.
- **Receive Email:** Emails from the user's inbox are displayed, allowing users to read them.
- **Delete Email:** Users can delete emails from their inbox.
- **Navigation:** Users can navigate through received emails using "Previous" and "Next" buttons.
- **Refresh:** Users can refresh the inbox to fetch the latest emails.

## Dependencies
- Python 3.x
- Tkinter (usually comes pre-installed with Python)
- `smtplib` (for sending emails)
- `imaplib` (for receiving emails)

## Usage
1. Run the script `email_client.py`.
2. Upon running, the application will prompt for the user's email address and password to log in.
3. Once logged in, the user can compose emails by filling in the recipient, subject, and email body fields, and clicking on the "Send Email" button.
4. Received emails will be displayed in the main window. Users can navigate through them using the "Previous" and "Next" buttons.
5. Users can delete emails by selecting them and clicking on the "Delete Email" button.
6. To refresh the inbox, click on the "Refresh" button.

## Configuration
- **Email Providers:** Although the current version of the email client is configured to work with WP Mail, you can modify the `server` variable in the `login` method of the `EmailClient` class according to your email provider's settings. Ensure that your email provider supports IMAP and SMTP protocols.

## Contributions
Contributions to improve the functionality, user interface, or fix any bugs are welcome. Please feel free to fork the repository, make your changes, and submit a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
