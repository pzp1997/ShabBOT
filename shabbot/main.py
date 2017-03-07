#!/usr/bin/env python

"""Helps coordinate Shabbat meals in the Orthodox Community at Penn (OCP)."""

import random

from shabbot import database_helper

__author__ = "Palmer Paul"
__version__ = "1.0.0"
__email__ = "pzpaul2002@yahoo.com"
__status__ = "Development"

NUM_MEALS = 1
SIZE_OF_MEAL = 2
MESSAGE = '''Hello!\n\n
    I am the OCP Shab-bot. Each week, I automatically invite twelve random
    OCPeople to Shabbat Lunch. This week, my algorithms have smiled down
    upon you.\n\n
    Please reply-all with what you are bringing (someone/s claim the main),
    and arrange a place to eat. Unfortunately I will not be able to make
    it, because I have SmarterChild\'s bot-mitzvah this weekend and also
    because my digestive system is made of javascript.\n\n
    This week\'s randomly generated meal theme is (U.S. season 7).\n\n
    Enjoy, and let me know how this goes! Always looking to update my
    programming and oil my joints.\n\n'''


@database_helper.ocp_database_required
def retrieve_student_emails(db_conn=None):
    """
    Retrieve email addresses of students from the MySQL database.

    Returns:
        A list of email addresses of people in the OCP.
    """
    query = 'SELECT email FROM subscriber WHERE grad_year > 2016'
    cursor = db_conn.cursor()
    cursor.execute(query)
    return list(cursor)


def email_invitees(invitees):
    """
    Email the invited guests.

    Args:
        invitees: a list of emails of those who are invited to the meal
    """
    print list(invitees)


def make_meals(emails):
    """
    Randomly select people to invite to meals.

    Args:
        emails: a list of email addresses of potential invitees
    Returns:
        A list of the people who were invited to meals
    """
    invitees = random.sample(emails, SIZE_OF_MEAL * NUM_MEALS)

    # Email invitees
    for i in range(0, invitees, SIZE_OF_MEAL):
        email_invitees(invitees[i:i+SIZE_OF_MEAL])

    return invitees


def main():
    """
    Entry point for the script.
    """
    students = retrieve_student_emails()

    invitees = make_meals(students)


if __name__ == '__main__':
    main()
