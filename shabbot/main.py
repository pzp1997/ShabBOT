#!/usr/bin/env python

"""Helps coordinate Shabbat meals in the Orthodox Community at Penn (OCP)."""

import itertools
import logging
import operator
import os.path
import random

from shabbot import database_helper
from shabbot import email_helper

__author__ = "Palmer Paul"
__email__ = "pzpaul2002@yahoo.com"
__version__ = "1.0.0"

NUM_MEALS = 1
SIZE_OF_MEAL = 10

MESSAGE = """
Hello!\n
I am the OCP Shab-bot. Each week, I automatically invite twelve random
OCPeople to Shabbat Lunch. This week, my algorithms have smiled down
upon you.\n
Please reply-all with what you are bringing (someone/s claim the main),
and arrange a place to eat. Unfortunately I will not be able to make
it, because I have SmarterChild's bot-mitzvah this weekend and also
because my digestive system is made of javascript.\n
This week's randomly generated meal theme is (U.S. season 7).\n
Enjoy, and let me know how this goes! Always looking to update my
programming and oil my joints.\n"""


def retrieve_student_emails(db_conn):
    """
    Retrieve email addresses of students from the MySQL database.

    Args:
        db_conn: an open MySQL database connection to retrieve the emails from
    Returns:
        A list of one-tuples of email addresses of people in the OCP
    """
    query = '''SELECT email FROM subscriber
        WHERE grad_year > 2016 AND email IS NOT NULL'''
    cursor = db_conn.cursor()
    cursor.execute(query)
    out = cursor.fetchall()
    cursor.close()
    return out


def make_meals(emails):
    """
    Randomly select people to invite to meals.

    Args:
        emails: a list of email addresses of potential invitees
    Returns:
        A list of meals, where each meal is a tuple of email addresses
    """
    random_emails = random.sample(emails, SIZE_OF_MEAL * NUM_MEALS)
    invitees = itertools.imap(operator.itemgetter(0), random_emails)

    meals = []
    for _ in xrange(NUM_MEALS):
        meal = tuple(itertools.islice(invitees, SIZE_OF_MEAL))
        meals.append(meal)
    return meals


def main():
    """
    Entry point for the script.
    """
    log_file_path = os.path.abspath(os.path.join(
        os.path.dirname(__file__), '..', 'shabbot.log'))

    logging.basicConfig(filename=log_file_path,
                        level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s',
                        datefmt='%m-%d-%y %H:%M')

    logging.info('Starting Shab-bot.')

    db_conn = database_helper.connect_to_mysql(
        database_helper.get_mysql_config())

    logging.info('Retrieving student email addresses.')
    students = retrieve_student_emails(db_conn)

    logging.info('Making randomized meals.')
    meals = make_meals(students)

    user, password = email_helper.get_email_config()
    mail = email_helper.login(user, password)

    logging.info('Sending invites for meals.')
    for meal in meals:
        logging.debug('Invitees: %s.', ', '.join(meal))
        email_helper.send_invite(mail, user, meal, MESSAGE)

    mail.quit()

    logging.info('Goodbye!')


if __name__ == '__main__':
    main()
