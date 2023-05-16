import os
import sys
import string
import random
import hashlib
import sys
import re
from getpass import getpass

from dbconfig import dbconfig

#Check if database with proper tables have been created
def checkConfig():
    db = dbconfig()
    cursor = db.cursor()
    query = "SELECT name FROM sqlite_master WHERE type='table' AND name='secrets'"
    cursor.execute(query)
    results = cursor.fetchall()
    db.close()
    if len(results)!=0:
        return True
    return False

# Generate device secret (salt)
def generateDeviceSecret(length=10):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k = length))

# Create database for master password
def make(password, confirm_password):
    if checkConfig():
        return False

    # Password validation
    if password != confirm_password:
        raise ValueError("Passwords do not match.")
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters long.")
    if not re.search(r'[A-Z]', password):
        raise ValueError("Password must contain at least one uppercase letter.")
    if not re.search(r'[a-z]', password):
        raise ValueError("Password must contain at least one lowercase letter.")
    if not re.search(r'\d', password):
        raise ValueError("Password must contain at least one digit.")
    if not re.search(r'[!@#$%^&+=?]', password):
        raise ValueError("Password must contain at least one special character (!@#$%^&+=?).")

    # Create tables
    db = dbconfig()
    cursor = db.cursor()
    query = "CREATE TABLE secrets (masterkey_hash TEXT NOT NULL, device_secret TEXT NOT NULL)"
    res = cursor.execute(query)

    query = "CREATE TABLE entries (sitename TEXT NOT NULL, siteurl TEXT NOT NULL, email TEXT, username TEXT, password TEXT NOT NULL)"
    res = cursor.execute(query)

    #Create variables for brute force prevention
    query = "CREATE TABLE variables (max_attempts INT NOT NULL, attempts INT NOT NULL, lockout_time INT NOT NULL)"
    res = cursor.execute(query)
    query = "INSERT INTO variables (max_attempts, attempts, lockout_time) values (3, 0, 5)"
    res = cursor.execute(query)
    db.commit()

    # Hash the MASTER PASSWORD
    hashed_mp = hashlib.sha256(password.encode()).hexdigest()

    # Generate a device secret
    ds = generateDeviceSecret()

    # Add them to db
    query = "INSERT INTO secrets (masterkey_hash, device_secret) values (?, ?)"
    val = (hashed_mp, ds)
    cursor.execute(query, val)
    db.commit()

    os.system('attrib +h pm.db') # Set file as hidden

    db.close()

    return True

# Function to delete account and drop all the tables
def delete():
    db = dbconfig()
    cursor = db.cursor()
    query = "DROP TABLE IF EXISTS secrets"
    cursor.execute(query)
    query = "DROP TABLE IF EXISTS entries"
    cursor.execute(query)
    query = "DROP TABLE IF EXISTS variables"
    cursor.execute(query)
    db.commit()
    db.close()
    os.remove('pm.db')
