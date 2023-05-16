import unittest
import sqlite3
from add import addEntry
from dbconfig import dbconfig

class TestAddEntry(unittest.TestCase):

    def setUp(self):
        # create an in-memory database for testing
        self.db = sqlite3.connect(':memory:')
        self.cursor = self.db.cursor()
        self.cursor.execute('CREATE TABLE entries (sitename TEXT, siteurl TEXT, email TEXT, username TEXT, password TEXT)')

    def test_add_entry_success(self):
        mp = "password"
        ds = "salt"
        sitename = "example"
        siteurl = "https://www.example.com"
        email = "test@example.com"
        username = "testuser"
        password = "testpassword"
        confirm_password = "testpassword"

        addEntry(mp, ds, sitename, siteurl, email, username, password, confirm_password)

        db = dbconfig()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM entries WHERE sitename=?", (sitename,))
        result = cursor.fetchone()

        self.assertIsNotNone(result)
        self.assertEqual(result[0], sitename)
        self.assertEqual(result[1], siteurl)
        self.assertEqual(result[2], email)
        self.assertEqual(result[3], username)
        self.assertIsNotNone(result[4])

    def test_add_entry_missing_required_fields(self):
        # test adding an entry with a missing required field
        with self.assertRaises(ValueError):
            addEntry("my_password", "my_data_source", "", "https://www.example.com", "", "", "mypassword", "mypassword")

    def test_add_entry_invalid_siteurl_format(self):
        # test adding an entry with an invalid siteurl format
        with self.assertRaises(ValueError):
            addEntry("my_password", "my_data_source", "example.com", "not_a_url", "user@example.com", "myusername", "mypassword", "mypassword")

    def test_add_entry_invalid_email_format(self):
        # test adding an entry with an invalid email format
        with self.assertRaises(ValueError):
            addEntry("my_password", "my_data_source", "example.com", "https://www.example.com", "invalid_email", "myusername", "mypassword", "mypassword")

    def test_add_entry_passwords_do_not_match(self):
        # test adding an entry with passwords that do not match
        with self.assertRaises(ValueError):
            addEntry("my_password", "my_data_source", "example.com", "https://www.example.com", "user@example.com", "myusername", "mypassword", "notmypassword")

    def tearDown(self):
        # close the database connection after each test
        self.db.close()

if __name__ == '__main__':
    unittest.main()



