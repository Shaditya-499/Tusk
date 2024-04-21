# import the required libraries
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os.path
import base64
from bs4 import BeautifulSoup
import csv

# Define the SCOPES. If modifying it, delete the token.pickle file.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
email_data_file_path = "email_data.csv"
if os.path.exists('tusk_email_data.csv'):
    first_time = False
message_ids = []
subjects = []
senders = []
messages = []

if os.path.exists(email_data_file_path):
    with open(email_data_file_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        first = True
        for row in reader:
            # Assuming each row contains Message-ID, Subject, From, and Message
            if first:
                first = False
                pass
            else:
                message_id = row[0]
                message_ids.append(message_id)
                subject = row[1]
                subjects.append(subject)
                sender = row[2]
                senders.append(sender)
                message = row[3]
                messages.append(message)

r_email_data = zip(message_ids, subjects, senders, messages)


def getEmails():
    # Variable creds will store the user access token.
    # If no valid token found, we will create one.
    creds = None

    # The file token.pickle contains the user access token.
    # Check if it exists
    if os.path.exists('token.pickle'):

        # Read the token from the file and store it in the variable creds
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If credentials are not available or are invalid, ask the user to log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the access token in token.pickle file for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    # Connect to the Gmail API
    service = build('gmail', 'v1', credentials=creds)

    # request a list of all the messages
    result = service.users().messages().list(userId='me').execute()

    # We can also pass maxResults to get any number of emails. Like this:
    result = service.users().messages().list(maxResults=500, userId='me').execute()
    messages = result.get('messages')

    # messages is a list of dictionaries where each dictionary contains a message id.
    IDs = []
    Subjects = []
    Senders = []
    Messages = []

    # iterate through all the messages
    for msg in messages:
        # Get the message from its id
        txt = service.users().messages().get(
            userId='me', id=msg['id']).execute()

        # Use try-except to avoid any Errors
        try:
            # Get value of 'payload' from dictionary 'txt'
            payload = txt['payload']
            headers = payload['headers']

            # Look for Subject and Sender Email in the headers
            for d in headers:
                if d['name'] == 'Subject':
                    subject = d['value']
                if d['name'] == 'From':
                    sender = d['value']
                if d['name'] == 'Message-ID':
                    id = d['value']

            if id in message_ids:
                break

            # The Body of the message is in Encrypted format. So, we have to decode it.
            # Get the data and decode it with base 64 decoder.
            parts = payload.get('parts')[0]
            data = parts['body']['data']
            data = data.replace("-", "+").replace("_", "/")
            decoded_data = base64.b64decode(data)

            # Now, the data obtained is in lxml. So, we will parse
            # it with BeautifulSoup library
            soup = BeautifulSoup(decoded_data, "lxml")
            body = soup.body()

            # Printing the subject, sender's email and message
            print("Message-ID: ", id)
            IDs.append(id)
            print("Subject: ", subject)
            Subjects.append(subject)
            print("From: ", sender)
            Senders.append(sender)
            print("Message: ", body)
            Messages.append(body)
            print('\n')
        except:
            pass

    email_data = zip(IDs, Subjects, Senders, Messages)

    # Write the email data to the CSV file
    with open(email_data_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        # Write header row
        writer.writerow(['Message-ID', 'Subject', 'From', 'Message'])
        # Write data rows
        for row in email_data:
            writer.writerow(row)
        for row in r_email_data:
            writer.writerow(row)


getEmails()
