
"""Automated tests for SmartBrew account registration and login."""

import os
import sqlite3
import tempfile
import unittest
from unittest.mock import patch

import accounts
import database


class TestAccounts(unittest.TestCase):
    """Test account registration and login using a temporary database."""

    def setUp(self):
        """Create an isolated temporary database for each test."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(
            self.temp_dir.name, "test_smartbrew.db"
        )
        self.connections = []

        self.database_patcher = patch.object(
            database, "DATABASE_NAME", self.db_path
        )
        self.accounts_patcher = patch.object(
            accounts, "get_connection", self.get_test_connection
        )

        
        self.database_patcher = patch.object(
             database, "DATABASE_NAME", self.db_path
        )
        self.accounts_patcher = patch.object(
             accounts, "get_connection", self.get_test_connection
        )
        self.database_connection_patcher = patch.object(
            database, "get_connection", self.get_test_connection
        )


        self.database_patcher.start()
        self.accounts_patcher.start()
        self.database_connection_patcher.start()
        database.initialize_database()

    def get_test_connection(self):
        """Open and track a connection to the test database."""
        connection = sqlite3.connect(self.db_path)
        self.connections.append(connection)
        return connection

    def tearDown(self):
        """Close tracked connections and restore patched functions."""
        for connection in self.connections:
            try:
                connection.close()
            except sqlite3.Error:
                pass

        self.accounts_patcher.stop()
        self.database_connection_patcher.stop()
        self.database_patcher.stop()
        self.temp_dir.cleanup()

    def test_create_account_successfully(self):
        """Confirm valid details create an account."""
        success, message = accounts.create_account(
            "testuser", "password123"
        )
        self.assertTrue(success)
        self.assertEqual(message, "Account created successfully.")

    def test_duplicate_username_is_rejected(self):
        """Prevent duplicate usernames."""
        accounts.create_account("testuser", "password123")
        success, message = accounts.create_account(
            "testuser", "anotherpass123"
        )
        self.assertFalse(success)
        self.assertEqual(message, "That username is already taken.")

    def test_username_is_trimmed(self):
        """Allow login after registration with surrounding spaces."""
        success, _ = accounts.create_account(
            "  testuser  ", "password123"
        )
        self.assertTrue(success)
        self.assertIsNotNone(
            accounts.authenticate_user("testuser", "password123")
        )

    def test_empty_username_is_rejected(self):
        """Reject registration with an empty username."""
        success, message = accounts.create_account(
            "   ", "password123"
        )
        self.assertFalse(success)
        self.assertEqual(message, "Username and password are required.")

    def test_empty_password_is_rejected(self):
        """Reject registration with an empty password."""
        success, message = accounts.create_account("testuser", "")
        self.assertFalse(success)
        self.assertEqual(message, "Username and password are required.")

    def test_short_password_is_rejected(self):
        """Reject passwords shorter than eight characters."""
        success, message = accounts.create_account("testuser", "short7")
        self.assertFalse(success)
        self.assertEqual(
            message, "Password must contain at least 8 characters."
        )

    def test_login_with_correct_password(self):
        """Confirm correct credentials return a user ID."""
        accounts.create_account("testuser", "password123")
        user_id = accounts.authenticate_user("testuser", "password123")
        self.assertIsNotNone(user_id)

    def test_login_with_incorrect_password(self):
        """Reject an incorrect password."""
        accounts.create_account("testuser", "password123")
        user_id = accounts.authenticate_user("testuser", "wrongpassword")
        self.assertIsNone(user_id)

    def test_login_with_unknown_username(self):
        """Reject login for an unknown username."""
        user_id = accounts.authenticate_user(
            "unknownuser", "password123"
        )
        self.assertIsNone(user_id)


if __name__ == "__main__":
    unittest.main()
