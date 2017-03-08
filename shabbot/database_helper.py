import ConfigParser
import os.path

import mysql.connector


def get_mysql_config():
    """
    Get credentials and settings for MySQL database. Data is stored in
    ShabBOT/config.cfg under the MYSQL section.

    Returns:
        A dictionary of configuration settings and credentials for MySQL DB
    """
    config = ConfigParser.ConfigParser()
    config.read(os.path.abspath(os.path.join(
        os.path.dirname(__file__), '..', 'config.cfg')))

    conf = config.items('MYSQL')
    conf.append(('raise_on_warnings', True))

    return dict(conf)


def connect_to_mysql(config):
    """
    Try to connect to MySQL database with given configuration settings.

    Args:
        config: configuration/credentials of the database
    Returns:
        A MySQL connection for the database
    """
    try:
        return mysql.connector.connect(**config)
    except mysql.connector.Error as err:
        print err
        exit(1)
