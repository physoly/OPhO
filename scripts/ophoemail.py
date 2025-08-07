import csv
import smtplib
import time
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import html

logging.basicConfig(
    filename='email_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# The mail addresses and password
sender_address = 'EMAIL'
sender_pass = 'PASSWORD'

# SMTP server settings
smtp_server = 'smtp.gmail.com'
smtp_port = 587

# Start a SMTP session
session = smtplib.SMTP(smtp_server, smtp_port)
session.starttls()  # enable security

# Login to the session
try:
    session.login(sender_address, sender_pass)
    logging.info('Successfully logged in to SMTP server.')
except smtplib.SMTPAuthenticationError as e:
    logging.error(f'Login failed: {e}')
    raise


# Read the CSV file
with open('opho-2-logins.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header

    for row in reader:
        receiver_address, username, password = row[0], row[1], row[2]

        escaped_username = html.escape(username)
        escaped_password = html.escape(password)

        # Setup the MIME
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = receiver_address
        message['Subject'] = 'Your Online Physics Olympiad Login Information'

        # The body of the email
        mail_content = f"""
Hello OPhO Team Leader,<br><br>

Here is your login information for the Online Physics Olympiad starting on August 7, 12 AM UTC. You may access the login page <a href='https://opho.physoly.tech/login'>here</a>.<br><br>

<b>Username:</b> {escaped_username}<br>
<b>Password:</b> {escaped_password}<br><br>

You may share these with the rest of your team so they can log in as well but do not share them with anyone else. Please note that the submission portal will not be open until the contest starts, meaning you will not be able to log in or access the portal until the contest begins. After the contest begins, go to "Submission Portal" to begin entering your answers. Please let us know if you have any issues logging in.<br><br>

In addition, please periodically check <a href='https://opho.physoly.tech/announcements'>https://opho.physoly.tech/announcements</a> for important info regarding the contest. Also, feel free to join our discord server: <a href='https://discord.gg/phods'>https://discord.gg/phods</a>.<br><br>

Good luck!<br>

The Online Physics Olympiad Committee<br><br>

For more contests like this, check out the <a href='https://physicsbrawl.org/'>Online Physics Brawl</a> in the Fall!
"""
        message.attach(MIMEText(mail_content, 'html'))  # use 'html' instead of 'plain'

        # Send the email



        try:
            text = message.as_string()
            session.sendmail(sender_address, receiver_address, text)
            logging.info(f"Email sent to {receiver_address} (username: {username})")
        except Exception as e:
            logging.error(f"Failed to send email to {receiver_address}: {e}")

        time.sleep(1) # maybe helps with rate limit idk

# Quit the session
session.quit()
logging.info("SMTP session ended.")
