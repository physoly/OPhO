import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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
session.login(sender_address, sender_pass)

# Read the CSV file
with open('opho-2-logins.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header

    for row in reader:
        receiver_address, username, password = row[0], row[1], row[2]

        # Setup the MIME
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = receiver_address
        message['Subject'] = 'Your Online Physics Olympiad Login Information'

        # The body of the email
        mail_content = f"""
Hello OPhO Team Leader,<br><br>

Here is your login information for the Online Physics Olympiad. You may access the login page <a href='https://opho.physoly.tech/login'>here</a>.<br><br>

<b>Username:</b> {username}<br>
<b>Password:</b> {password}<br><br>

You may share these with the rest of your team so they can log in as well but do not share them with anyone else. Please note that the submission portal will not be open until the contest starts. After the contest begins, go to "Submission Portal" to begin entering your answers. Please let us know if you have any issues logging in.<br><br>

In addition, please periodically check <a href='https://opho.physoly.tech/announcements'>https://opho.physoly.tech/announcements</a> for important info regarding the contest. Also, feel free to join our discord server: <a href='https://discord.gg/phods'>https://discord.gg/phods</a>.<br><br>

Good luck!<br>

The Online Physics Olympiad Committee
"""
        message.attach(MIMEText(mail_content, 'html'))  # use 'html' instead of 'plain'

        # Send the email
        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)

# Quit the session
session.quit()
