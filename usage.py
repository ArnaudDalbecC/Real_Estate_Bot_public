from main import send_email
from chat import chatbot

receiver_email = 'receiver@gmail.com'
# Set the subject of the email
subject = 'Test email'

# Read the HTML template
with open('index.html', 'r') as file:
    html_template = file.read()

# List of recipients and their messages
recipients = [
    {"name": "John", "message": "This is your first message."},
]

subject = "Personalized Email"

for recipient in recipients:
    # Customize the HTML body
    custom_body = html_template.format(name=recipient["name"], message=recipient["message"])
    
    # Send the email
    send_email(receiver_email, subject, custom_body, pdf_path=None, is_html=True)
    print(custom_body)
    
if __name__ == "__main__":
   bot = chatbot()
   bot.main()