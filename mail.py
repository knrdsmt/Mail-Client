import smtplib
import imaplib
from email.mime.text import MIMEText
import tkinter as tk
from tkinter import messagebox, scrolledtext, Entry, Label

class EmailClient:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Email Client")
        self.root.geometry("600x800")

        self.email_text = scrolledtext.ScrolledText(self.root, wrap=tk.WORD)
        self.email_text.pack(fill=tk.BOTH, expand=True)

        recipient_label = Label(self.root, text="Email address:")
        recipient_label.pack()
        self.recipient_entry = Entry(self.root)
        self.recipient_entry.pack()

        subject_label = Label(self.root, text="Subject:")
        subject_label.pack()
        self.subject_entry = Entry(self.root)
        self.subject_entry.pack()

        send_button = tk.Button(self.root, text="Send Email", command=self.send_email)
        send_button.pack()

        receive_button = tk.Button(self.root, text="Receive Email", command=self.receive_email)
        receive_button.pack()

        self.previous_button = tk.Button(self.root, text="Previous", state=tk.DISABLED, command=self.show_previous_email)
        self.previous_button.pack(side=tk.LEFT)

        self.next_button = tk.Button(self.root, text="Next", state=tk.DISABLED, command=self.show_next_email)
        self.next_button.pack(side=tk.RIGHT)

        self.email_ids = []
        self.current_email_index = None
        self.mail = None

    def send_email(self):
        # Logowanie do serwera SMTP
        server = 'smtp.wp.pl'
        user = 'konradsiem@wp.pl'
        password = 'Klolol0202'

        session = smtplib.SMTP(server, 587)
        session.starttls()
        session.login(user, password)

        # Wysyłanie e-maila
        recipients = [self.recipient_entry.get()]
        sender = 'konradsiem@wp.pl'
        subject = self.subject_entry.get()
        body = self.email_text.get("1.0", tk.END)

        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = ', '.join(recipients)

        session.sendmail(sender, recipients, msg.as_string())
        session.quit()
        messagebox.showinfo("Email Sent", "Email sent successfully!")

    def receive_email(self):
        # Logowanie do serwera IMAP
        self.mail = imaplib.IMAP4_SSL('imap.wp.pl')
        self.mail.login('konradsiem@wp.pl', 'Klolol0202')
        self.mail.select('inbox')

        # Odbieranie e-maili
        result, data = self.mail.search(None, 'ALL')
        self.email_ids = data[0].split()

        if not self.email_ids:
            messagebox.showinfo("No Emails", "No emails found in the inbox.")
            return

        self.current_email_index = len(self.email_ids) - 1
        self.show_current_email()

    def show_current_email(self):
        if self.current_email_index is not None and 0 <= self.current_email_index < len(self.email_ids):
            email_id = self.email_ids[self.current_email_index]
            result, data = self.mail.fetch(email_id, '(BODY[HEADER.FIELDS (FROM SUBJECT)])')
            raw_email_header = data[0][1].decode('utf-8')

            sender_start = raw_email_header.find("From:") + 6
            sender_end = raw_email_header.find("\r\n", sender_start)
            sender = raw_email_header[sender_start:sender_end].strip()

            subject_start = raw_email_header.find("Subject:") + 9
            subject_end = raw_email_header.find("\r\n", subject_start)
            subject = raw_email_header[subject_start:subject_end].strip()

            self.email_text.delete("1.0", tk.END)
            self.email_text.insert(tk.END, f"From: {sender}\nSubject: {subject}\n\n")

            result, data = self.mail.fetch(email_id, '(RFC822.TEXT)')
            raw_email_text = data[0][1].decode('utf-8')
            self.email_text.insert(tk.END, raw_email_text)

            self.email_text.insert(tk.END, "\n\n" + "_" * 70)

            self.previous_button["state"] = tk.NORMAL if self.current_email_index > 0 else tk.DISABLED
            self.next_button["state"] = tk.NORMAL if self.current_email_index < len(self.email_ids) - 1 else tk.DISABLED

    def show_previous_email(self):
        if self.current_email_index is not None and self.current_email_index > 0:
            self.current_email_index -= 1
            self.show_current_email()

    def show_next_email(self):
        if self.current_email_index is not None and self.current_email_index < len(self.email_ids) - 1:
            self.current_email_index += 1
            self.show_current_email()

    def run(self):
        self.root.mainloop()
        if self.mail:
            self.mail.logout()

if __name__ == '__main__':
    client = EmailClient()
    client.run()
