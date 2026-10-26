
"""Account registration and login for SmartBrew AI."""

import hashlib
import hmac
import secrets
import sqlite3

from database import get_connection, initialize_database


def hash_password(password):
    """Hash a password before storing it.

    Inputs:
        password: The password entered by the user.

    Returns:
        A string containing the salt and password hash.
    """
    salt = secrets.token_hex(16)
    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        200_000,
    ).hex()

    return f"{salt}${password_hash}"


def verify_password(password, stored_hash):
    """Check whether a password matches its stored hash.

    Inputs:
        password: The password entered during login.
        stored_hash: The salt and hash saved in the database.

    Returns:
        True if the password matches, otherwise False.
    """
    try:
        salt, expected_hash = stored_hash.split("$", 1)
    except ValueError:
        return False

    actual_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        200_000,
    ).hex()

    return hmac.compare_digest(actual_hash, expected_hash)


def create_account(username, password):
    """Register a new user account.

    Inputs:
        username: The name chosen by the user.
        password: The password chosen by the user.

    Returns:
        A tuple containing whether registration succeeded and a message.
    """
    username = username.strip()

    if not username or not password:
        return False, "Username and password are required."

    if len(password) < 8:
        return False, "Password must contain at least 8 characters."

    connection = get_connection()

    try:
        cursor = connection.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, hash_password(password)),
        )
        user_id = cursor.lastrowid

        connection.execute(
            "INSERT INTO preferences (user_id) VALUES (?)",
            (user_id,),
        )

        connection.commit()
        return True, "Account created successfully."

    except sqlite3.IntegrityError:
        connection.rollback()
        return False, "That username is already taken."

    finally:
        connection.close()


def authenticate_user(username, password):
    """Check login details and return the user's ID if valid.

    Inputs:
        username: The username entered during login.
        password: The password entered during login.

    Returns:
        The user's ID if login succeeds, otherwise None.
    """
    connection = get_connection()

    try:
        row = connection.execute(
            "SELECT id, password_hash FROM users WHERE username = ?",
            (username.strip(),),
        ).fetchone()

        if row and verify_password(password, row[1]):
            return row[0]

        return None

    finally:
        connection.close()


if __name__ == "__main__":
    initialize_database()

    print("SmartBrew AI account test")
    choice = input("Choose register or login: ").strip().lower()
    username = input("Username: ")
    password = input("Password: ")

    if choice == "register":
        success, message = create_account(username, password)
        print(message)

    elif choice == "login":
        user_id = authenticate_user(username, password)

        if user_id is not None:
            print(f"Login successful. User ID: {user_id}")
        else:
            print("Invalid username or password.")

    else:
        print("Please enter register or login.")
