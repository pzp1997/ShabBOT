import ConfigParser
from functools import wraps
import os.path

import mysql.connector

def get_mysql_config():
    """
    Get credentials and settings for MySQL database. Data is stored in
    ShabBOT/config.cfg under the MYSQL section.

    Returns:
        A dictionary of configuration settings and credentials for MySQL DB.
    """
    config = ConfigParser.ConfigParser()
    config.read(os.path.abspath(os.path.join(
        os.path.dirname(__file__), '..', 'config.cfg')))

    conf = config.items('MYSQL')
    conf.append(('raise_on_warnings', True))

    return dict(conf)


def connect_to_db(config):
    """
    Try to connect to MySQL database with given configuration settings.

    Returns:
        A MySQL connection for the database
    """
    try:
        return mysql.connector.connect(**config)
    except mysql.connector.Error as err:
        print err
        exit(1)


def database_required(config):
    """
    Decorator to ensure that a function has an open database connection.
    """
    cnx = connect_to_db(config)
    def decorator(func):
        @wraps(func)
        def inner(*args, **kwargs):
            if not cnx.is_connected():
                cnx = connect_to_db(config)
            kwargs['db_conn'] = cnx
            return func(*args, **kwargs)
        return inner
    return decorator

ocp_database_required = database_required(get_mysql_config())
