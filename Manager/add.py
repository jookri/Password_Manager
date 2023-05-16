from getpass import getpass
from dbconfig import dbconfig
import aesutil
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512
from Crypto.Random import get_random_bytes
import base64
import re

# Compute masterkey with PBKDF2 using hashed masterpassword and device secret
def computeMasterKey(mp,ds):
	password = mp.encode()
	salt = ds.encode()
	key = PBKDF2(password, salt, 32, count=1000000, hmac_hash_module=SHA512)
	return key

# Add password to database
def addEntry(mp, ds, sitename, siteurl, email, username, password, confirm_password):
    if not sitename and not siteurl:
        raise ValueError("Either sitename or URL address is missing.")

    if sitename and len(sitename) > 64:
        raise ValueError("Sitename must not exceed 64 characters.")

    if username and len(username) > 64:
        raise ValueError("Username must not exceed 64 characters.")

    if siteurl and len(siteurl) > 2048:
        raise ValueError("Siteurl must not exceed 2048 characters.")

    if not email and not username:
        raise ValueError("Either email or username is missing.")

    if email and len(email) > 256:
        raise ValueError("Email must not exceed 254 characters.")

    if not password:
        raise ValueError("Password is required.")

    if password != confirm_password:
        raise ValueError("Passwords do not match.")

    if siteurl and not re.match(r'^(?:http|ftp)s?://|www\.|[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+|\w+\.\w+$',
                                siteurl):
        raise ValueError("Invalid siteurl format.")

    if email and not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        raise ValueError("Invalid email format.")

    if any(c.isspace() for c in sitename + siteurl + email + username):
        raise ValueError("Spaces are not allowed in any other fields than password")

    mk = computeMasterKey(mp, ds)

    #encrypt password
    encrypted = aesutil.encrypt(key=mk, source=password, keyType="bytes")

    # Add to db
    db = dbconfig()
    cursor = db.cursor()
    query = "INSERT INTO entries (sitename, siteurl, email, username, password) values (?, ?, ?, ?, ?)"
    val = (sitename, siteurl, email, username, encrypted)
    cursor.execute(query, val)
    db.commit()
