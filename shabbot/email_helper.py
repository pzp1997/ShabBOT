import ConfigParser
from email.mime.text import MIMEText
import os.path
import smtplib


def get_email_config():
    """
    Get credentials for Shab-bot Gmail account. Data is stored in
    ShabBOT/config.cfg under the SHABBOT_EMAIL section.

    Returns:
        A tuple with the username and password for the Gmail account
    """
    config = ConfigParser.ConfigParser()
    config.read(os.path.abspath(os.path.join(
        os.path.dirname(__file__), '..', 'config.cfg')))

    user = config.get('SHABBOT_EMAIL', 'USER')
    password = config.get('SHABBOT_EMAIL', 'PASSWORD')

    return (user, password)


def login(user, password):
    """
    Login to Gmail.

    Args:
        user: Gmail username
        password: Gmail password
    Returns:
        A connection to Gmail that can be used for sending emails
    """
    mail = smtplib.SMTP('smtp.gmail.com', 587)
    mail.ehlo()
    mail.starttls()
    mail.ehlo()  # should call ehlo again after starttls
    mail.login(user, password)
    return mail


def send_invite(mail, user, invitees, message):
    """
    Email the invited guests.

    Args:
        mail: an email connection to send the invite from
        user: the email address to send the invite from
        invitees: a list of emails of those who are invited to the meal
        message: the body of the email, in this case the invitation
    """
    sender = 'OCP Shab-bot <{}>'.format(user)
    recipients = ', '.join(invitees)

    msg = MIMEText(message)
    msg['Subject'] = 'Shab-bot Lunch'
    msg['From'] = sender
    msg['To'] = recipients

    mail.sendmail(user, invitees, msg.as_string())
