import imaplib
import email
from email.header import decode_header
import os

# Outlook IMAP details
EMAIL_ACCOUNT = "cbms.smfg@buildint.co"
EMAIL_PASSWORD = "CSBuildint@2024"  # Use an App Password if 2FA is enabled

IMAP_SERVER = "outlook.office365.com"
IMAP_PORT = 993

# Connect to the Outlook IMAP server
mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)

# Select the mailbox (Inbox)
mail.select("inbox")

# Search for emails with PDF attachments
status, messages = mail.search(None, 'ALL')

# Convert message numbers to a list
mail_ids = messages[0].split()

# Directory to save PDFs
SAVE_DIR = "C:/Users/Computer Point/OneDrive/Desktop/E-Bill Downloader/PDFs"
os.makedirs(SAVE_DIR, exist_ok=True)

for mail_id in mail_ids:
    # Fetch email data
    status, msg_data = mail.fetch(mail_id, "(RFC822)")
    
    for response_part in msg_data:
        if isinstance(response_part, tuple):
            msg = email.message_from_bytes(response_part[1])
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding or "utf-8")

            # Check for attachments
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    filename = part.get_filename()
                    
                    if filename and filename.endswith(".pdf"):
                        filename = decode_header(filename)[0][0]
                        if isinstance(filename, bytes):
                            filename = filename.decode("utf-8")

                        filepath = os.path.join(SAVE_DIR, filename)
                        with open(filepath, "wb") as f:
                            f.write(part.get_payload(decode=True))
                        print(f"Downloaded: {filename}")

# Logout
mail.logout()
