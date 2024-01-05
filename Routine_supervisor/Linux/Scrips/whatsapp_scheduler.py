import os
from datetime import datetime, timedelta
import time
from twilio.rest import Client

# Twilio credentials
account_sid = 'your_account_sid'
auth_token = 'your_auth_token'
twilio_phone_number = 'your_twilio_phone_number'
your_phone_number = 'your_phone_number'

# Create Twilio client
client = Client(account_sid, auth_token)

# File paths for events
base_path = os.path.dirname(os.path.abspath(__file__))
database_directory_path = os.path.join(base_path, 'Database')
events_file_path = os.path.join(database_directory_path, 'events.txt')
modified_events_file_path = os.path.join(database_directory_path, 'modified_events.txt')

# Create text files if they don't exist
text_files = [
    'events.txt', 'modified_events.txt',
    'maintenance_mode_actions.txt', 'power_loss_actions.txt',
    'deleted_messages_log.txt', 'messages.txt'
]

for file in text_files:
    file_path = os.path.join(database_directory_path, file)
    if not os.path.exists(file_path):
        with open(file_path, 'w') as text_file:
            text_file.write("")


def send_whatsapp_message(message):
    message = client.messages.create(
        body=message,
        from_='whatsapp:{}'.format(twilio_phone_number),
        to='whatsapp:{}'.format(your_phone_number)
    )

    print("WhatsApp message sent:", message.sid)


def read_events_from_file(file_path):
    events = []
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            events = file.read().splitlines()
    return events


def write_events_to_file(file_path, events):
    with open(file_path, 'w') as file:
        file.write('\n'.join(events))


def handle_event(day, time, message):
    current_day = datetime.now().strftime('%A')
    current_time = datetime.now().strftime('%H:%M')

    if current_day.lower() == day.lower() and current_time == time:
        send_whatsapp_message(message)


def handle_interruption():
    if os.path.exists('maintenance_mode.txt'):
        send_whatsapp_message("Routine Supervisor has successfully entered Maintenance Mode.")
        with open('maintenance_mode_actions.txt', 'a') as log_file:
            log_file.write("Maintenance Mode actions performed at {}\n".format(datetime.now()))

    if os.path.exists('power_loss.txt'):
        send_whatsapp_message("Routine Supervisor has detected a power loss.")
        with open('power_loss_actions.txt', 'a') as log_file:
            log_file.write("Power loss actions performed at {}\n".format(datetime.now()))


def delete_messages_at_midnight():
    now = datetime.now()
    midnight = datetime(now.year, now.month, now.day, 0, 0)
    midnight_delta = midnight + timedelta(days=1) - now
    time.sleep(midnight_delta.total_seconds())

    with open('deleted_messages_log.txt', 'a') as log_file:
        log_file.write("Messages deleted at midnight on {}\n".format(datetime.now()))

    delete_messages_from_file()


def delete_media_files_at_midnight():
    now = datetime.now()
    midnight = datetime(now.year, now.month, now.day, 0, 0)
    midnight_delta = midnight + timedelta(days=1) - now
    time.sleep(midnight_delta.total_seconds())

    with open('deleted_messages_log.txt', 'a') as log_file:
        log_file.write("Media files deleted at midnight on {}\n".format(datetime.now()))

    delete_media_files_from_directory()


def delete_messages_from_file():
    try:
        with open('messages.txt', 'w') as messages_file:
            messages_file.write("")

    except Exception as e:
        print("Error deleting messages from the file:", e)


def delete_media_files_from_directory():
    media_directory = 'media_files'
    try:
        for filename in os.listdir(media_directory):
            file_path = os.path.join(media_directory, filename)
            if is_media_file(file_path):
                os.remove(file_path)
                print("Deleted media file:", file_path)

    except Exception as e:
        print("Error deleting media files:", e)


def is_media_file(file_path):
    media_extensions = ['.gif', '.jpg', '.jpeg', '.png']
    _, file_extension = os.path.splitext(file_path)
    return file_extension.lower() in media_extensions


def add_event_to_file(event):
    # Read existing events from the file
    events = read_events_from_file(events_file_path)

    # Append the new event
    events.append(event)

    # Write the updated events to the file
    write_events_to_file(events_file_path, events)


def add_message_to_file(message):
    with open('messages.txt', 'a') as messages_file:
        messages_file.write("{} | {}\n".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), message))

def main_routine():
    handle_interruption()

    # Read events from the file
    events = read_events_from_file(events_file_path)

    # Handle each event
    for event in events:
        day, time, message = event.split('|')
        handle_event(day.strip(), time.strip(), message.strip())

    on_campus_message = "NOTE: Any event scheduled between 8:00 AM - 17:00 PM will be overwritten when attending " \
                        "lectures on-campus, studying, completing MCQs and Assignments or any other activities " \
                        "involving my studies at Damelin. Any overwritten events will replace tomorrow’s morning " \
                        "events between 4:41 – 7:42 AM."

    received_message = input("Enter your command: ")

    if "On-Campus" in received_message:
        send_whatsapp_message(on_campus_message)

    elif "Off-Campus" in received_message:
        # Revert to the normal schedule by clearing any modifications
        reset_schedule()
        print("Reverted to the normal schedule.")

    elif received_message.startswith("Add Event"):
        # Add a new event
        new_event = received_message[len("Add Event "):].strip()
        add_event_to_file(new_event)

        print("Event added:", new_event)

def reset_schedule():
    # Read existing events from the file
    events = read_events_from_file(events_file_path)

    # Filter out events added during the "On-Campus" scenario
    filtered_events = [event for event in events if "On-Campus" not in event]

    # Write the updated events to the file
    write_events_to_file(events_file_path, filtered_events)

    # Additional actions, if needed
    # You can add more logic here based on your requirements
    print("Cleared events added during the 'On-Campus' scenario.")
   

# Main function
def main():
    current_script_path = os.path.dirname(os.path.abspath(__file__))
    base_path = os.path.join(current_script_path, '...')  # Moves up 2 levels to the Routine_supervisor folder

    # Define the path for the 'Database' directory
    database_directory_path = os.path.join(base_path, 'Database')

    # Create 'Database' directory if it doesn't existimport os
from datetime import datetime, timedelta
import time
from twilio.rest import Client

# Twilio credentials
account_sid = 'your_account_sid'
auth_token = 'your_auth_token'
twilio_phone_number = 'your_twilio_phone_number'
your_phone_number = 'your_phone_number'

# Create Twilio client
client = Client(account_sid, auth_token)

# File paths for events
base_path = os.path.dirname(os.path.abspath(__file__))
database_directory_path = os.path.join(base_path, 'Database')
events_file_path = os.path.join(database_directory_path, 'events.txt')
modified_events_file_path = os.path.join(database_directory_path, 'modified_events.txt')

# Create text files if they don't exist
text_files = [
    'events.txt', 'modified_events.txt',
    'maintenance_mode_actions.txt', 'power_loss_actions.txt',
    'deleted_messages_log.txt', 'messages.txt'
]

for file in text_files:
    file_path = os.path.join(database_directory_path, file)
    if not os.path.exists(file_path):
        with open(file_path, 'w') as text_file:
            text_file.write("")


def send_whatsapp_message(message):
    message = client.messages.create(
        body=message,
        from_='whatsapp:{}'.format(twilio_phone_number),
        to='whatsapp:{}'.format(your_phone_number)
    )

    print("WhatsApp message sent:", message.sid)


def read_events_from_file(file_path):
    events = []
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            events = file.read().splitlines()
    return events


def write_events_to_file(file_path, events):
    with open(file_path, 'w') as file:
        file.write('\n'.join(events))


def handle_event(day, time, message):
    current_day = datetime.now().strftime('%A')
    current_time = datetime.now().strftime('%H:%M')

    if current_day.lower() == day.lower() and current_time == time:
        send_whatsapp_message(message)


def handle_interruption():
    if os.path.exists('maintenance_mode.txt'):
        send_whatsapp_message("Routine Supervisor has successfully entered Maintenance Mode.")
        with open('maintenance_mode_actions.txt', 'a') as log_file:
            log_file.write("Maintenance Mode actions performed at {}\n".format(datetime.now()))

    if os.path.exists('power_loss.txt'):
        send_whatsapp_message("Routine Supervisor has detected a power loss.")
        with open('power_loss_actions.txt', 'a') as log_file:
            log_file.write("Power loss actions performed at {}\n".format(datetime.now()))


def delete_messages_at_midnight():
    now = datetime.now()
    midnight = datetime(now.year, now.month, now.day, 0, 0)
    midnight_delta = midnight + timedelta(days=1) - now
    time.sleep(midnight_delta.total_seconds())

    with open('deleted_messages_log.txt', 'a') as log_file:
        log_file.write("Messages deleted at midnight on {}\n".format(datetime.now()))

    delete_messages_from_file()


def delete_media_files_at_midnight():
    now = datetime.now()
    midnight = datetime(now.year, now.month, now.day, 0, 0)
    midnight_delta = midnight + timedelta(days=1) - now
    time.sleep(midnight_delta.total_seconds())

    with open('deleted_messages_log.txt', 'a') as log_file:
        log_file.write("Media files deleted at midnight on {}\n".format(datetime.now()))

    delete_media_files_from_directory()


def delete_messages_from_file():
    try:
        with open('messages.txt', 'w') as messages_file:
            messages_file.write("")

    except Exception as e:
        print("Error deleting messages from the file:", e)


def delete_media_files_from_directory():
    media_directory = 'media_files'
    try:
        for filename in os.listdir(media_directory):
            file_path = os.path.join(media_directory, filename)
            if is_media_file(file_path):
                os.remove(file_path)
                print("Deleted media file:", file_path)

    except Exception as e:
        print("Error deleting media files:", e)


def is_media_file(file_path):
    media_extensions = ['.gif', '.jpg', '.jpeg', '.png']
    _, file_extension = os.path.splitext(file_path)
    return file_extension.lower() in media_extensions


def add_event_to_file(event):
    # Read existing events from the file
    events = read_events_from_file(events_file_path)

    # Append the new event
    events.append(event)

    # Write the updated events to the file
    write_events_to_file(events_file_path, events)


def add_message_to_file(message):
    with open('messages.txt', 'a') as messages_file:
        messages_file.write("{} | {}\n".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), message))


def create_profile(profile_name):
    profile_path = os.path.join(database_directory_path, f'{profile_name}.txt')
    
    if not os.path.exists(profile_path):
        with open(profile_path, 'w') as profile_file:
            profile_file.write("No events scheduled here...")
        send_whatsapp_message(f"Profile '{profile_name}' created successfully.")
    else:
        send_whatsapp_message(f"Profile '{profile_name}' already exists. Please choose a different name.")


def rename_profile(old_name, new_name):
    old_profile_path = os.path.join(database_directory_path, f'{old_name}.txt')
    new_profile_path = os.path.join(database_directory_path, f'{new_name}.txt')
    
    if os.path.exists(old_profile_path):
        os.rename(old_profile_path, new_profile_path)
        send_whatsapp_message(f"Profile '{old_name}' renamed to '{new_name}'.")
    else:
        send_whatsapp_message(f"Profile '{old_name}' does not exist. Cannot rename.")


def main_routine():
    handle_interruption()

    # Read events from the file
    events = read_events_from_file(events_file_path)

    # Handle each event
    for event in events:
        day, time, message = event.split('|')
        handle_event(day.strip(), time.strip(), message.strip())

    on_campus_message = "NOTE: Any event scheduled between 8:00 AM - 17:00 PM will be overwritten when attending " \
                        "lectures on-campus, studying, completing MCQs and Assignments or any other activities " \
                        "involving my studies at Damelin. Any overwritten events will replace tomorrow’s morning " \
                        "events between 4:41 – 7:42 AM."

    received_message = input("Enter your command: ")

    if received_message.startswith("Create Profile"):
        profile_name = received_message[len("Create Profile "):].strip()
        create_profile(profile_name)

    elif received_message.startswith("Rename Profile"):
        old_name, new_name = received_message[len("Rename Profile "):].strip().split(',')
        rename_profile(old_name.strip(), new_name.strip())

    elif "On-Campus" in received_message:
        send_whatsapp_message(on_campus_message)

    elif "Off-Campus" in received_message:
        # Revert to the normal schedule by clearing any modifications
        reset_schedule()
        print("Reverted to the normal schedule.")


def reset_schedule():
    # Read existing events from the file
    events = read_events_from_file(events_file_path)

    # Filter out events added during the "On-Campus" scenario
    filtered_events = [event for event in events if "On-Campus" not in event]

    # Write the updated events to the file
    write_events_to_file(events_file_path, filtered_events)

    # Additional actions, if needed
    # You can add more logic here based on your requirements
    print("Cleared events added during the 'On-Campus' scenario.")


# Main function
def main():
    current_script_path = os.path.dirname(os.path.abspath(__file__))
    base_path = os.path.join(current_script_path, '...')  # Moves up 2 levels to the Routine_supervisor folder

    # Define the path for the 'Database' directory
    database_directory_path = os.path.join(base_path, 'Database')

    # Create 'Database' directory if it doesn't exist
    if not os.path.exists(database_directory_path):
        os.makedirs(database_directory_path)

    # Create text files if they don't exist
    text_files = ['events.txt', 'modified_events.txt', 'maintenance_mode_actions.txt', 'power_loss_actions.txt',
                  'deleted_messages_log.txt', 'messages.txt']
    for file in text_files:
        file_path = os.path.join(database_directory_path, file)
        if not os.path.exists(file_path):
            with open(file_path, 'w') as text_file:
                text_file.write("")

    # Add events to the 'events.txt' file
    events_content = """
    Monday | 08:00 | Meeting with Team
    Tuesday | 12:30 | Lunch with Client
    Wednesday | 10:00 | Project Presentation
    """
    with open(os.path.join(database_directory_path, 'events.txt'), 'w') as events_file:
        events_file.write(events_content)


if __name__ == "__main__":
    main()
    delete_messages_at_midnight()
    delete_media_files_at_midnight()

    while True:
        main_routine()

    if not os.path.exists(database_directory_path):
        os.makedirs(database_directory_path)

    # Create text files if they don't exist
    text_files = ['events.txt', 'modified_events.txt', 'maintenance_mode_actions.txt', 'power_loss_actions.txt',
                  'deleted_messages_log.txt', 'messages.txt']
    for file in text_files:
        file_path = os.path.join(database_directory_path, file)
        if not os.path.exists(file_path):
            with open(file_path, 'w') as text_file:
                text_file.write("")

    # Add events to the 'events.txt' file
    events_content = """
    Monday | 08:00 | Meeting with Team
    Tuesday | 12:30 | Lunch with Client
    Wednesday | 10:00 | Project Presentation
    """
    with open(os.path.join(database_directory_path, 'events.txt'), 'w') as events_file:
        events_file.write(events_content)
        


if __name__ == "__main__":
    main()
    delete_messages_at_midnight()
    delete_media_files_at_midnight()

    while True:
        main_routine()
