import ConfigParser
import os.path

import mysql.connector

config = ConfigParser.ConfigParser()
config.read(os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', 'config.cfg')))

mysql_config = config.items('MYSQL')
mysql_config.append(('raise_on_warnings', True))

try:
    dbConn = mysql.connector.connect(**dict(mysql_config))
except mysql.connector.Error as err:
    print err
    exit(1)

cursor = dbConn.cursor()
emails = cursor.execute("SELECT email FROM subscriber WHERE grad_year > 2016")

print emails
