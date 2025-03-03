import os
from html import unescape
import random

from bs4 import BeautifulSoup
from bs4.element import NavigableString
from email.parser import BytesParser
from email import policy
import codecs
import csv


def decode_payload(part):
    """Decodes email body, handling Quoted-Printable encoding if necessary."""
    payload = part.get_payload(decode=True)  # Decode base64/QP if needed
    charset = sanitize_charset(part.get_content_charset() or 'utf-8')

    try:
        decoded_text = payload.decode(charset, errors='replace')
    except (UnicodeDecodeError, TypeError):
        decoded_text = payload.decode('latin-1', errors='replace')

    return decoded_text


def sanitize_charset(charset):
    if not charset:
        return "utf-8"

    charset = charset.strip().lower()
    try:
        codecs.lookup(charset)
        return charset
    except LookupError:
        return "utf-8"


def html_to_plain_text(html):
    soup = BeautifulSoup(html, 'html.parser')
    if soup.head:
        soup.head.decompose()
    for a_tag in soup.find_all('a'):
        a_text = a_tag.get_text(strip=True)
        a_tag.replace_with(NavigableString(f"HYPERLINK {a_text}"))
    text = soup.get_text(separator='\n', strip=True)  # type: ignore
    text = unescape(text)
    text = '\n'.join(line.strip() for line in text.splitlines() if line.strip())
    text = f"\n{text}\n"
    return text


def extract_email_content(file_path):
    with open(file_path, 'rb') as f:
        msg = BytesParser(policy=policy.default).parse(f)
    subject = msg["subject"]
    body = ''
    if msg.is_multipart():
        for part in msg.iter_parts():
            if part.get_content_type() == 'text/plain' and not body:
                body = decode_payload(part)
                break
            elif part.get_content_type() == 'text/html' and not body:
                body = html_to_plain_text(decode_payload(part))
                break
    else:
        try:
            body = decode_payload(msg)
            if msg.get_content_type() == 'text/html':
                body = html_to_plain_text(body)
        except (UnicodeDecodeError, TypeError) as e:
            print(f"Error decoding non-multipart email: {e}")
            body = 'Error decoding non-multipart email.'

    return subject, body


def process_email_directory(directory, is_spam):
    """
    Process all email files in a directory and assign spam labels.
    """
    email_data = []
    for filename in sorted(os.listdir(directory)):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            subject, body = extract_email_content(file_path)
            email_data.append({'subject': subject, 'body': body, 'is_spam': is_spam})
    return email_data


## SAVE AS CSV
def save_emails_to_csv(ham_list, spam_list, output_file):
    all_emails = ham_list + spam_list
    random.shuffle(all_emails)

    # Save shuffled data to CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['subject', 'body', 'is_spam']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for entry in all_emails:
            writer.writerow({'subject': entry['subject'], 'body': entry['body'], 'is_spam': entry['is_spam']})

# Directory paths
easy_ham_dir = '../data/easy_ham'
easy_spam_dir = '../data/easy_spam'

# Process emails
ham_emails = process_email_directory(easy_ham_dir, is_spam=False)
spam_emails = process_email_directory(easy_spam_dir, is_spam=True)

output_csv = '../data/emails.csv'
save_emails_to_csv(ham_emails, spam_emails, output_csv)
print(f"Emails saved to {output_csv}")


# Print sample emails
print("Ham Emails:")
for email in ham_emails[:5]:
    print(f"Subject: {email['subject']}\nBody: {email['body']}\n")

print("Spam Emails:")
for email in spam_emails[:5]:
    print(f"Subject: {email['subject']}\nBody: {email['body']}\n")
