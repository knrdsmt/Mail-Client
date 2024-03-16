import smtplib
import imaplib
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, scrolledtext, Entry, Label
from email.mime.text import MIMEText

class EmailClient:
    def __init__(self):
        self.password = None
        self.user = None
        self.root = tk.Tk()
        self.root.title("Email Client")
        self.root.geometry("800x600")

        self.style = ttk.Style()
        self.style.theme_use("clam")  # You can change the theme to your preference

        self.email_text = scrolledtext.ScrolledText(self.root, wrap=tk.WORD)
        self.email_text.pack(fill=tk.BOTH, expand=True)

        input_frame = ttk.Frame(self.root)
        input_frame.pack(pady=10)

        recipient_label = Label(input_frame, text="Recipient:")
        recipient_label.grid(row=0, column=0, padx=5, pady=5)
        self.recipient_entry = Entry(input_frame)
        self.recipient_entry.grid(row=0, column=1, padx=5, pady=5)

        subject_label = Label(input_frame, text="Subject:")
        subject_label.grid(row=1, column=0, padx=5, pady=5)
        self.subject_entry = Entry(input_frame)
        self.subject_entry.grid(row=1, column=1, padx=5, pady=5)

        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=5)

        refresh_button = ttk.Button(button_frame, text="Refresh", command=self.receive_email)
        refresh_button.grid(row=0, column=2, padx=5, pady=5)

        send_button = ttk.Button(button_frame, text="Send Email", command=self.send_email)
        send_button.grid(row=0, column=0, padx=5, pady=5)

        self.delete_button = ttk.Button(button_frame, text="Delete Email", state=tk.DISABLED, command=self.delete_email)
        self.delete_button.grid(row=0, column=1, padx=5, pady=5)

        nav_frame = ttk.Frame(self.root)
        nav_frame.pack(pady=5)

        self.previous_button = ttk.Button(nav_frame, text="Previous", state=tk.DISABLED, command=self.show_previous_email)
        self.previous_button.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.next_button = ttk.Button(nav_frame, text="Next", state=tk.DISABLED, command=self.show_next_email)
        self.next_button.grid(row=0, column=1, padx=5, pady=5, sticky="e")

        self.email_ids = []
        self.current_email_index = None
        self.mail = None

        self.login()

    def login(self):
        server = 'imap.wp.pl'
        self.user = simpledialog.askstring("Login", "Enter your email address:")
        self.password = simpledialog.askstring("Login", "Enter your email password:", show='*')

        try:
            self.mail = imaplib.IMAP4_SSL(server)
            self.mail.login(self.user, self.password)
            self.mail.select('inbox')
            self.receive_email()
        except imaplib.IMAP4.error as e:
            messagebox.showerror("Login Error", "Invalid credentials. Please check your email address and password.")
            self.root.destroy()

    def send_email(self):
        server = 'smtp.wp.pl'

        session = smtplib.SMTP(server, 587)
        session.starttls()
        session.login(self.user, self.password)

        recipients = [self.recipient_entry.get()]
        sender = self.user
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

            self.previous_button["state"] = tk.NORMAL if self.current_email_index > 0 else tk.DISABLED
            self.next_button["state"] = tk.NORMAL if self.current_email_index < len(self.email_ids) - 1 else tk.DISABLED
            self.delete_button["state"] = tk.NORMAL

    def delete_email(self):
        if self.current_email_index is not None and 0 <= self.current_email_index < len(self.email_ids):
            email_id = self.email_ids[self.current_email_index]
            self.mail.store(email_id, '+FLAGS', '(\Deleted)')
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

    def run(self):
        self.root.mainloop()
        if self.mail:
            self.mail.logout()

if __name__ == '__main__':
    client = EmailClient()
    client.run()
