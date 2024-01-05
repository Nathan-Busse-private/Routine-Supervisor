import os
from datetime import datetime
from twilio.rest import Client

# Set up Twilio client (you need to sign up for Twilio and get your credentials)
account_sid = 'your_account_sid'
auth_token = 'your_auth_token'
whatsapp_from = 'whatsapp:+14155238886'
whatsapp_to = 'whatsapp:+1234567890'
client = Client(account_sid, auth_token)

# Function to send messages via WhatsApp
def send_whatsapp_message(message):
    message = client.messages.create(
        body=message,
        from_=whatsapp_from,
        to=whatsapp_to
    )
    return message.sid

# Function to detect power loss
def detect_power_loss():
    if os.path.exists('power_loss.txt'):
        send_whatsapp_message("Routine Supervisor has detected a power loss. Power loss detected at {}".format(datetime.now()))

if __name__ == "__main__":
    detect_power_loss()
    # Perform power loss recovery tasks
    # ...
