from dbconfig import dbconfig
import aesutil
import hashlib

from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512
from Crypto.Random import get_random_bytes
from getpass import getpass

# Compute masterkey with PBKDF2 using hashed masterpassword and device secret
def computeMasterKey(mp,ds):
	password = mp.encode()
	salt = ds.encode()
	key = PBKDF2(password, salt, 32, count=1000000, hmac_hash_module=SHA512)
	return key

# copy password to the clipboard
def copy_password(password):
	results = get_mp_ds()
	# Compute master key
	mk = computeMasterKey(results[0], results[1])

	# decrypt password
	decrypted = aesutil.decrypt(key=mk, source=password, keyType="bytes")

	return decrypted.decode()

#get master password and device secret
def get_mp_ds():
	db = dbconfig()
	cursor = db.cursor()
	query = "SELECT * FROM secrets"
	cursor.execute(query)
	result = cursor.fetchall()[0]
	return result

#delete password from database
def delete_entry(password):
	db = dbconfig()
	cursor = db.cursor()
	cursor.execute("DELETE FROM entries WHERE password=%s", (password,))
	db.commit()

#get passwords from database
def retrieve_entries():
	db = dbconfig()
	cursor = db.cursor()
	cursor.execute("SELECT * FROM entries")
	result = cursor.fetchall()
	return result

# function to get the maximum number of login attempts from the variables table
def get_max_attempts():
	db = dbconfig()
	cursor = db.cursor()
	cursor.execute("SELECT max_attempts FROM variables")
	result = cursor.fetchone()
	return result[0]

# function to update the login attempts in the variables table
def update_attempts(attempts):
	db = dbconfig()
	cursor = db.cursor()
	cursor.execute("UPDATE variables SET attempts = ?", (attempts,))
	db.commit()

# function to get the total number of login attempts from the variables table
def get_attempts():
	db = dbconfig()
	cursor = db.cursor()
	cursor.execute("SELECT attempts FROM variables")
	result = cursor.fetchone()
	return result[0]

# function to get the lockout time from the variables table
def get_lockout_time():
	db = dbconfig()
	cursor = db.cursor()
	cursor.execute("SELECT lockout_time FROM variables")
	result = cursor.fetchone()
	return result[0]

# function to update the lockout time in the variables table
def update_lockout_time(new_time):
	db = dbconfig()
	cursor = db.cursor()
	cursor.execute("UPDATE variables SET lockout_time = ?", (new_time,))
	db.commit()

# check if masterpassword is correct
def ValidateMasterPassword(mp):
	hashed_mp = hashlib.sha256(mp.encode()).hexdigest()
	db = dbconfig()
	cursor = db.cursor()
	query = "SELECT * FROM secrets"
	cursor.execute(query)
	result = cursor.fetchall()[0]
	if hashed_mp != result[0]:
		return False
	return True

def delete_entry(password):
	db = dbconfig()
	cursor = db.cursor()
	cursor.execute("DELETE FROM entries WHERE password=?", (password,))
	db.commit()

	db.close()