import pathlib
import textwrap

import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown

import csv
import json

from to_json import make_json


def readCSV(filename):
    with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
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


def to_markdown(text):
    text = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))


# Or use `os.getenv('GOOGLE_API_KEY')` to fetch an environment variable.
GOOGLE_API_KEY = 'AIzaSyAYMPXUnpAIoCv-9ZGtA6bm-7DdE-YP1_0'

genai.configure(api_key=GOOGLE_API_KEY)


model = genai.GenerativeModel('gemini-pro')
print(f"Using model : {model}")

messages = []
message_ids = []
subjects = []
senders = []
tusk_responses = []
# Example usage:
readCSV('email_data.csv')

for i in range(30):
    message = messages[i]
    tusk_response_object = model.generate_content(
        "here's the Email i have received , if it specifies some work which i need to do, return the summarized work . if no work, then return 'No tasks'" + message)
    tusk_response = tusk_response_object.text
    tusk_responses.append(tusk_response)

tusk_email_data = zip(message_ids[0:30], subjects[0:30],
                      senders[0:30], messages[0:30], tusk_responses[0:30])

# Write the email data to the CSV file
with open("tusk_email_data.csv", 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    # Write header row
    writer.writerow(['Message-ID', 'Subject', 'From',
                    'Message', 'Tusk-Response'])
    # Write data rows
    for row in tusk_email_data:
        writer.writerow(row)

csvFilePath = r'tusk_email_data.csv'
jsonFilePath = r'tusk_email_data.json'

# Call the make_json function
make_json(csvFilePath, jsonFilePath)
