import pathlib
import textwrap

import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown

import csv
import os
import json

# from to_json import make_json


def read_email_data(email_data):
    with open(email_data, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        first = True
        for row in reader:
            # Assuming each row contains Message-ID, Subject, From, and Message
            if first:
                first = False
                pass
            else:
                if row[0] not in rmessage_ids:
                    message_id = row[0]
                    message_ids.append(message_id)
                    subject = row[1]
                    subjects.append(subject)
                    sender = row[2]
                    senders.append(sender)
                    message = row[3]
                    messages.append(message)
                else:
                    break


def read_tusk_email_data(tusk_email_data):
    with open(tusk_email_data, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        first = True
        for row in reader:
            # Assuming each row contains Message-ID, Subject, From, and Message
            if first:
                first = False
                pass
            else:
                rmessage_id = row[0]
                rmessage_ids.append(rmessage_id)
                rsubject = row[1]
                rsubjects.append(rsubject)
                rsender = row[2]
                rsenders.append(rsender)
                rmessage = row[3]
                rmessages.append(rmessage)
                rtusk_response = row[4]
                rtusk_responses.append(rtusk_response)


def to_markdown(text):
    text = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))


# Or use `os.getenv('GOOGLE_API_KEY')` to fetch an environment variable.
GOOGLE_API_KEY = 'AIzaSyAYMPXUnpAIoCv-9ZGtA6bm-7DdE-YP1_0'

first_time = True
if os.path.exists('tusk_email_data.csv'):
    first_time = False

genai.configure(api_key=GOOGLE_API_KEY)


model = genai.GenerativeModel('gemini-pro')
print(f"Using model : {model}")

messages = []
message_ids = []
subjects = []
senders = []
tusk_responses = []
rmessage_ids = []
rsubjects = []
rsenders = []
rmessages = []
rtusk_responses = []
# Example usage:
if not first_time:
    read_tusk_email_data('tusk_email_data.csv')
    r_tusk_email_data = zip(rmessage_ids, rsubjects,
                            rsenders, rmessages, rtusk_responses)
read_email_data('email_data.csv')
print(message_ids)

for msg in messages:
    tusk_response_object = model.generate_content(
        "have i revieved any instructions to follow in this message?  ->" + msg)
    tusk_response = tusk_response_object.text
    tusk_responses.append(tusk_response)

tusk_email_data = zip(message_ids, subjects,
                      senders, messages, tusk_responses)

# Write the email data to the CSV file
with open("tusk_email_data.csv", 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    # Write header row
    writer.writerow(['Message-ID', 'Subject', 'From', 'Message', 'Tusk-Response'])
    # Write data rows
    for row in tusk_email_data:
        writer.writerow(row)
    for row in r_tusk_email_data:
        writer .writerow(row)

csvFilePath = r'tusk_email_data.csv'
jsonFilePath = r'tusk_email_data.json'

# Call the make_json function
# make_json(csvFilePath, jsonFilePath)
