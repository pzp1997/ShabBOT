#!/usr/bin/env python

"""Helps coordinate Shabbat meals in the Orthodox Community at Penn (OCP)."""

import itertools
import numpy as np

import .database_helper

__author__ = "Palmer Paul"
__version__ = "1.0.0"
__email__ = "pzpaul2002@yahoo.com"
__status__ = "Development"

NUM_MEALS = 1
SIZE_OF_MEAL = 2
FREQUENCY_FACTOR = 4
MESSAGE = '\n\n'.join((
    'Hello!',
    'I am the OCP Shab-bot. Each week, I automatically invite twelve random '
    'OCPeople to Shabbat Lunch. This week, my algorithms have smiled down '
    'upon you.',
    'Please reply-all with what you are bringing (someone/s claim the main), '
    'and arrange a place to eat. Unfortunately I will not be able to make '
    'it, because I have SmarterChild\'s bot-mitzvah this weekend and also '
    'because my digestive system is made of javascript.',
    'This week\'s randomly generated meal theme is (U.S. season 7).',
    'Enjoy, and let me know how this goes! Always looking to update my '
    'programming and oil my joints.'
))


@database_helper.ocp_database_required
def retrieve_people(db_conn):
    """
    Retrieve OCPeople (and recency) from the MySQL database.

    Returns:
        A dictionary of OCPeople mapped to their recency.
    """
    query = 'SELECT email FROM subscriber WHERE grad_year > 2016'
    cursor = db_conn.cursor()
    cursor.execute(query)
    return list(cursor)


def normalize_freq(freqs):
    """
    Create a valid probability distribution that sums to one.

    Args:
        freqs: an integer list of frequencies
    Returns:
        A generator over the adjusted frequencies
    """
    total = float(sum(freqs))
    return (x / total for x in freqs)


def email_invitees(invitees):
    """
    Email the invited guests.

    Args:
        invitees: a list of emails of those who are invited to the meal
    """
    print list(invitees)


def make_meals(people):
    """
    Randomly select people to invite to meals.

    Args:
        people: a dictionary of people to select from mapped to their recency
    Returns:
        A list of the people who were invited to meals
    """
    #
    invitees = np.random.choice(people.keys(), SIZE_OF_MEAL * NUM_MEALS, False,
                                list(normalize_freq(people.values())))

    # Email invitees
    iter_invitees = iter(invitees)
    for _ in xrange(NUM_MEALS):
        email_invitees(itertools.islice(iter_invitees, SIZE_OF_MEAL))

    return invitees


def main():
    """
    Entry point for the script.
    """
    people = retrieve_people()

    invitees = make_meals(people)

    # Reset invitees recency
    for invitee in invitees:
        people[invitee] /= FREQUENCY_FACTOR

    # Increment everyones recency
    for person in people:
        people[person] += 1


if __name__ == '__main__':
    main()
