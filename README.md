# Email Client

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
1. **Install Python:** Make sure you have Python 3.x installed on your system.
2. **Clone Repository:** Clone the repository containing the email client application.
3. **Install Dependencies:** If necessary, install the required dependencies by running `pip install -r requirements.txt`.
4. **Run the Program:** Execute the script `email_client.py` by running `python email_client.py`.
5. **Login:** Upon running, the application will prompt for your email address and password to log in.
6. **Compose and Send Emails:** Once logged in, compose emails by filling in the recipient, subject, and email body fields, and click on the "Send Email" button.
7. **Read Received Emails:** Received emails will be displayed in the main window. Navigate through them using the "Previous" and "Next" buttons.
8. **Delete Emails:** Delete emails by selecting them and clicking on the "Delete Email" button.
9. **Refresh Inbox:** To refresh the inbox, click on the "Refresh" button.

## Configuration
- **Email Providers:** Although the current version of the email client is configured to work with WP Mail, you can modify the `server` variable in the `login` method of the `EmailClient` class according to your email provider's settings. Ensure that your email provider supports IMAP and SMTP protocols.

## Contributions
Contributions to improve the functionality, user interface, or fix any bugs are welcome. Please feel free to fork the repository, make your changes, and submit a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
