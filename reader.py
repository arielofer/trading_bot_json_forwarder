import os

from utils import clean, parse_message, parse_parts


def read_message(service, message):
    """
    This function takes Gmail API `service` and the given `message_id` and
    does the following:
        - Downloads the content of the email
        - Prints email basic information (To, From, Subject & Date) and
          plain/text parts

    deprecated features:
        - Creates a folder for each email based on the subject
        - Downloads text/html content (if available) and saves it under the
          folder created as index.html
        - Downloads any file that is attached to the email and saves it in the
          folder created
    """
    msg = service.users().messages().get(
        userId='me', id=message['id'], format='full').execute()
    # parts can be the message body, or attachments
    payload = msg['payload']
    parts = payload.get("parts")
    if parts:
        parse_parts(parts)
    else:
        parse_message(payload)
    print("="*50)
