import smtplib
import imaplib
from email.mime.text import MIMEText
import tkinter as tk
from tkinter import messagebox, scrolledtext, Entry, Label, Toplevel

class EmailClient:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Email Client")
        self.root.geometry("800x600")

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

        self.delete_button = tk.Button(self.root, text="Delete Email", state=tk.DISABLED, command=self.delete_email)
        self.delete_button.pack()

        self.previous_button = tk.Button(self.root, text="Previous", state=tk.DISABLED, command=self.show_previous_email)
        self.previous_button.pack(side=tk.LEFT)

        self.next_button = tk.Button(self.root, text="Next", state=tk.DISABLED, command=self.show_next_email)
        self.next_button.pack(side=tk.RIGHT)

        edit_autoresponder_button = tk.Button(self.root, text="Edit Autoresponder", command=self.edit_autoresponder)
        edit_autoresponder_button.pack()

        self.autoresponder_text = scrolledtext.ScrolledText(self.root, wrap=tk.WORD)
        self.autoresponder_text.insert(tk.END, "Thank you for your email. I have received your message and will get back to you as soon as possible.\n\nOriginal Message:\n")

        search_label = Label(self.root, text="Keyword to Search:")
        search_label.pack(side=tk.LEFT)

        self.search_entry = Entry(self.root)
        self.search_entry.pack(side=tk.LEFT)

        search_button = tk.Button(self.root, text="Search", command=self.search_email)
        search_button.pack(side=tk.LEFT)

        self.email_ids = []
        self.current_email_index = None
        self.mail = None

    def send_email(self):
        server = 'smtp.wp.pl'
        user = 'konradsiem@wp.pl'
        password = 'Klolol0202'

        session = smtplib.SMTP(server, 587)
        session.starttls()
        session.login(user, password)

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
        self.mail = imaplib.IMAP4_SSL('imap.wp.pl')
        self.mail.login('konradsiem@wp.pl', 'Klolol0202')
        self.mail.select('inbox')

        result, data = self.mail.search(None, 'ALL')
        self.email_ids = data[0].split()

        if not self.email_ids:
            messagebox.showinfo("No Emails", "No emails found in the inbox.")
            return

        self.current_email_index = len(self.email_ids) - 1
        self.show_current_email()

        # Dodanie autorespondera
        self.autoresponder()

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
            self.delete_button["state"] = tk.NORMAL

    def delete_email(self):
        if self.current_email_index is not None and 0 <= self.current_email_index < len(self.email_ids):
            email_id = self.email_ids[self.current_email_index]
            self.mail.store(email_id, '+FLAGS', '(\Del  eted)')
            self.mail.expunge()
            messagebox.showinfo("Email Deleted", "Email deleted successfully!")
            self.receive_email()

    def show_previous_email(self):
        if self.current_email_index is not None and self.current_email_index > 0:
            self.current_email_index -= 1
            self.show_current_email()

    def show_next_email(self):
        if self.current_email_index is not None and self.current_email_index < len(self.email_ids) - 1:
            self.current_email_index += 1
            self.show_current_email()

    def edit_autoresponder(self):
        edit_window = Toplevel(self.root)
        edit_window.title("Edit Autoresponder")
        edit_window.geometry("400x500")

        edit_autoresponder_text = scrolledtext.ScrolledText(edit_window, wrap=tk.WORD)
        edit_autoresponder_text.pack(fill=tk.BOTH, expand=True)

        current_autoresponder_text = self.autoresponder_text.get("1.0", tk.END)
        edit_autoresponder_text.insert(tk.END, current_autoresponder_text)

        save_button = tk.Button(edit_window, text="Save Changes", command=lambda: self.save_autoresponder_changes(edit_autoresponder_text, edit_window))
        save_button.pack()

    def save_autoresponder_changes(self, edited_text_widget, edit_window):
        # Zapisanie zmian do głównego okna
        new_autoresponder_text = edited_text_widget.get("1.0", tk.END)
        self.autoresponder_text.delete("1.0", tk.END)
        self.autoresponder_text.insert(tk.END, new_autoresponder_text)

        edit_window.destroy()

    def autoresponder(self):
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

            response_subject = f"Re: {subject}"
            response_body = self.autoresponder_text.get("1.0", tk.END)

            result, data = self.mail.fetch(email_id, '(RFC822.TEXT)')
            original_email_text = data[0][1].decode('utf-8')
            response_body += original_email_text

            self.send_response(sender, response_subject, response_body)

    def send_response(self, recipient, subject, body):
        server = 'smtp.wp.pl'
        user = 'konradsiem@wp.pl'
        password = 'Klolol0202'

        session = smtplib.SMTP(server, 587)
        session.starttls()
        session.login(user, password)

        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = user
        msg['To'] = recipient

        session.sendmail(user, [recipient], msg.as_string())
        session.quit()
        messagebox.showinfo("Autoresponder", f"Autoresponder response sent to {recipient}")

def search_email(self):
    keyword = self.search_entry.get()
    if not keyword:
        messagebox.showinfo("Search Error", "Please enter a keyword to search.")
        return

    matching_emails = []

    for email_id in self.email_ids:
        try:
            result, data = self.mail.fetch(email_id, '(RFC822.TEXT)')
            raw_email_text = data[0][1]

            # Use a more tolerant decoding approach (ignore errors)
            decoded_text = raw_email_text.decode('utf-8', errors='ignore')

            keyword_count = decoded_text.lower().count(keyword.lower())
            matching_emails.append((decoded_text, keyword_count))
        except UnicodeDecodeError as e:
            print(f"Error decoding email {email_id}: {e}")

    if matching_emails:
        # Find the email with the highest keyword count
        best_matching_email, _ = max(matching_emails, key=lambda item: item[1])

        self.email_text.delete("1.0", tk.END)
        self.email_text.insert(tk.END, best_matching_email)
    else:
        self.email_text.delete("1.0", tk.END)
        self.email_text.insert(tk.END, "No matching emails found.")

    def run(self):
        self.root.mainloop()
        if self.mail:
            self.mail.logout()

if __name__ == '__main__':
    client = EmailClient()
    client.run()