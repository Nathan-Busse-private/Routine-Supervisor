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

# Function to enter maintenance mode
def enter_maintenance_mode():
    with open('maintenance_mode.txt', 'w') as file:
        file.write("Entered Maintenance Mode at {}".format(datetime.now()))
    send_whatsapp_message("Routine Supervisor has successfully entered Maintenance Mode. Maintenance Mode engaged.")

# Function to exit maintenance mode
def exit_maintenance_mode():
    os.remove('maintenance_mode.txt')
    send_whatsapp_message("Routine Supervisor has successfully exited Maintenance Mode. Maintenance Mode disengaged.")

if __name__ == "__main__":
    enter_maintenance_mode()
    # Perform maintenance mode tasks
    # ...
    exit_maintenance_mode()
