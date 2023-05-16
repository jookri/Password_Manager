import sqlite3
import os

# Create and connect to the database
def dbconfig():
    try:
        db = sqlite3.connect('pm.db')
    except Exception as e:
        error_message = "An error occurred while trying to connect to the database: {}".format(e)
        raise ValueError(error_message)
        sys.exit(0)

    return db