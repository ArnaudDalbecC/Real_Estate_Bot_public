# Plain text content
import smtplib
import imaplib
import ssl
from email.message import EmailMessage
import mimetypes
import os
import re
import email
from chat import chatbot

# Define email sender and receiver
email_sender = os.environ.get('EMAIL_SENDER')
email_password = os.environ.get('EMAIL_PASSWORD')
email_receiver = 'arnauddalbec@gmail.com'

# Add SSL ( of security)
context = ssl.create_default_context()

IMAP_SERVER = "imap.gmail.com"

def send_email(email_receiver, subject, body, pdf_path=None, is_html=False): 
    em = EmailMessage()
    
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    
    if is_html:
        em.add_alternative(body, subtype='html')
    else:
        em.set_content(body)
    
    # Attach PDF if provided
    if pdf_path:
        # Guess the MIME type and subtype
        mime_type, _ = mimetypes.guess_type(pdf_path)
        mime_type, mime_subtype = mime_type.split('/')
        
        with open(pdf_path, 'rb') as pdf_file:
            em.add_attachment(pdf_file.read(),
                              maintype=mime_type,
                              subtype=mime_subtype,
                              filename=os.path.basename(pdf_path))
    
    # Log in and send the email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())
        

def check_email_replies():
    """Check inbox for replies and trigger a process."""
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(email_sender, email_password)
        mail.select("inbox")

        # Search for unread emails from the expected recipient
        status, messages = mail.search(None, '(UNSEEN FROM "{}")'.format(email_receiver))
        email_ids = messages[0].split()

        for e_id in email_ids:
            # Fetch the email
            status, msg_data = mail.fetch(e_id, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject = msg["subject"]
                    sender = msg["from"]
                    full_body = ""

                    # Extract full email conversation (including quoted replies)
                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == "text/plain":
                                full_body += part.get_payload(decode=True).decode()
                    else:
                        full_body = msg.get_payload(decode=True).decode()

                    print(f"Full Email Conversation from {sender}:\nSubject: {subject}\n\n{full_body}")

                    # Trigger a process with the full conversation
                    trigger_process(sender, subject, full_body)
        mail.logout()

    except Exception as e:
        print("Error checking email replies:", e)
        
def extract_bot_response(full_body):
    """Extract only the bot's response from the full email conversation."""
    match = re.search(r"\[/INST\](.*)", full_body, re.DOTALL)
    if match:
        return match.group(1).strip()
    return full_body

def trigger_process(sender, subject, body):
    """Define the process to be triggered upon receiving a reply."""
    print(f"Processing response from {sender}: {body}")
    
    # Generating response with the bot
    bot = chatbot()
    full_body = bot.main(body)
    bot_response = extract_bot_response(full_body)
    # Sending response
    send_email(email_receiver, subject, f"{bot_response}")

# Example Usage
if __name__ == "__main__":
    # Send an email
    #send_email(email_receiver, "Test Email", "Please reply to this email.")

    # Check for replies
    check_email_replies()