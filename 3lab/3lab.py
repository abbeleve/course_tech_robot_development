import smtplib as smt
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
import imaplib
from email.header import decode_header
import email as em

class EmailSender:

    def __init__(self, email, password, smtp_server = "smtp.gmail.com", port = 587):
        self.smtp_server = smtp_server
        self.port = port
        self.email = email
        self.password = password

    def send_email(self):
        from_email = self.email
        html, subject, to_email = self.read_from_json('3lab/info.json')
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = from_email
        message["To"] = to_email

        mimetext = MIMEText(html, "html")
        
        message.attach(mimetext)

        try:
            server = smt.SMTP(self.smtp_server, self.port)
            server.starttls()
            server.login(email, password)
            server.sendmail(from_email, to_email, message.as_string())
            print('email sended')
        except Exception as e:
            print(e)
        finally:
            server.quit()

    def read_from_json(self, json_path):
        with open(json_path, encoding="utf-8",) as f:
            json_file = json.load(f)

        return json_file["html"], json_file['subject'], json_file["to_email"]

email = "andreiprojectaleks@gmail.com"
password = "koij jzmu zkmx kbyb"
email_sender = EmailSender(email=email, password = password)

#HTML



class EmailReader:
    def __init__(self, email, password, IMAP_SERVER = "imap.gmail.com"):
        self.email = email
        self.password = password
        self.IMAP_SERVER = IMAP_SERVER

    def check_email_from_sender(self, sender_email):
        mail = imaplib.IMAP4_SSL(self.IMAP_SERVER)
        mail.login(self.email, self.password)
        mail.select("inbox")
        status, messages = mail.search(None, f'FROM "{sender_email}"')
        email_ids = messages[0].split()
        for i, email_id in enumerate(email_ids[:5]):
            status, msg_data = mail.fetch(email_id, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = em.message_from_bytes(response_part[1])

                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding if encoding else "utf-8")

                    from_ = msg.get("From")

                    print(f"\nПисьмо {i+1}")
                    print(f"От: {from_}")
                    print(f"Тема: {subject}")

                    mail.store(email_id, '+FLAGS', '\\Seen')

        mail.logout()

email_sender.send_email()
email_sender.read_from_json("3lab/info.json")

# email_checker = EmailReader(email, password)
# email_checker.check_email_from_sender("andreiprojectaleks@gmail.com")