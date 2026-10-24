
"""Database functions for the SmartBrew AI application."""

import sqlite3
from contextlib import contextmanager

DATABASE_NAME = "smartbrew.db"


@contextmanager
def database_connection():
    """Provide a database connection that closes after use.

    Yields:
        An SQLite connection. Changes are committed on success and
        rolled back if an exception occurs.
    """
    connection = get_connection()

    try:
        with connection:
            yield connection
    finally:
        connection.close()


def get_connection():
    """Open and return a connection to the SQLite database.

    Returns:
        An open SQLite database connection.
    """
    return sqlite3.connect(DATABASE_NAME)


def initialize_database():
    """Create all application tables if they do not already exist.

    Returns:
        None.
    """
    with database_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS preferences (
                user_id INTEGER PRIMARY KEY,
                coffee_strength TEXT NOT NULL DEFAULT 'Medium',
                milk TEXT NOT NULL DEFAULT 'Regular',
                temperature TEXT NOT NULL DEFAULT 'Hot',
                syrup TEXT NOT NULL DEFAULT 'None',
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS recipes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                beverage TEXT NOT NULL,
                coffee_strength TEXT NOT NULL,
                milk TEXT NOT NULL,
                temperature TEXT NOT NULL,
                syrup TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                beverage TEXT NOT NULL,
                order_details TEXT NOT NULL,
                amount REAL NOT NULL,
                payment_method TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ingredient TEXT UNIQUE NOT NULL,
                quantity REAL NOT NULL,
                threshold REAL NOT NULL
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS waste_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                waste_type TEXT NOT NULL,
                quantity REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)


def seed_inventory():
    """Add initial ingredient stock without overwriting existing stock.

    Returns:
        None.
    """
    initial_inventory = [
        ("Coffee", 500, 50),
        ("Water", 5000, 500),
        ("Milk", 2000, 200),
        ("Chocolate", 500, 50),
    ]

    with database_connection() as connection:
        connection.executemany("""
            INSERT OR IGNORE INTO inventory
                (ingredient, quantity, threshold)
            VALUES (?, ?, ?)
        """, initial_inventory)


def get_inventory():
    """Retrieve current quantities and thresholds for all ingredients.

    Returns:
        A dictionary keyed by ingredient name.
    """
    with database_connection() as connection:
        rows = connection.execute("""
            SELECT ingredient, quantity, threshold
            FROM inventory
            ORDER BY ingredient
        """).fetchall()

    return {
        ingredient: {
            "quantity": quantity,
            "threshold": threshold,
        }
        for ingredient, quantity, threshold in rows
    }


def refill_inventory(ingredient, quantity):
    """Add a positive quantity of an ingredient to the inventory.

    Args:
        ingredient: Name of the ingredient to refill.
        quantity: Positive quantity to add to the current stock.

    Returns:
        A tuple containing success status and a message.
    """
    if quantity <= 0:
        return False, "Refill quantity must be greater than zero."

    with database_connection() as connection:
        row = connection.execute(
            "SELECT quantity FROM inventory WHERE ingredient = ?",
            (ingredient,),
        ).fetchone()

        if row is None:
            return False, f"{ingredient} was not found in inventory."

        connection.execute(
            "UPDATE inventory SET quantity = quantity + ? "
            "WHERE ingredient = ?",
            (quantity, ingredient),
        )

    return True, f"Added {quantity:g} units of {ingredient}."


def log_waste(ingredient, quantity):
    """Record wasted stock and deduct it from inventory.

    Args:
        ingredient: Name of the ingredient that was wasted.
        quantity: Positive quantity of stock wasted.

    Returns:
        A tuple containing success status and a message.
    """
    if quantity <= 0:
        return False, "Waste quantity must be greater than zero."

    with database_connection() as connection:
        row = connection.execute(
            "SELECT quantity FROM inventory WHERE ingredient = ?",
            (ingredient,),
        ).fetchone()

        if row is None:
            return False, f"{ingredient} was not found in inventory."

        current_quantity = row[0]

        if quantity > current_quantity:
            return False, "Waste quantity cannot exceed available stock."

        connection.execute(
            "UPDATE inventory SET quantity = quantity - ? "
            "WHERE ingredient = ?",
            (quantity, ingredient),
        )

        connection.execute(
            "INSERT INTO waste_logs (waste_type, quantity) VALUES (?, ?)",
            (ingredient, quantity),
        )

    return True, f"Recorded {quantity:g} units of wasted {ingredient}."


def get_waste_logs():
    """Retrieve recorded waste entries, newest first.

    Returns:
        A list of dictionaries containing waste records.
    """
    with database_connection() as connection:
        rows = connection.execute("""
            SELECT id, waste_type, quantity, created_at
            FROM waste_logs
            ORDER BY created_at DESC, id DESC
        """).fetchall()

    columns = ["id", "waste_type", "quantity", "created_at"]

    return [dict(zip(columns, row)) for row in rows]


def check_ingredient_availability(ingredients):
    """Check whether an order can be made without breaching stock thresholds.

    Args:
        ingredients: Dictionary of ingredient names and required quantities.

    Returns:
        A tuple containing availability (bool) and a list of problems.
    """
    inventory = get_inventory()
    problems = []

    for ingredient, required in ingredients.items():
        if ingredient not in inventory:
            problems.append(f"{ingredient} is missing from inventory.")
            continue

        quantity = inventory[ingredient]["quantity"]
        threshold = inventory[ingredient]["threshold"]

        if required < 0:
            problems.append(
                f"Required quantity for {ingredient} cannot be negative."
            )
        elif quantity < required:
            problems.append(f"Not enough {ingredient}.")
        elif quantity - required < threshold:
            problems.append(
                f"Ordering would put {ingredient} below its minimum stock."
            )

    return len(problems) == 0, problems


def save_preferences(
    user_id, coffee_strength, milk, temperature, syrup
):
    """Save or update a user's drink preferences.

    Args:
        user_id: ID of the user.
        coffee_strength: Preferred coffee strength.
        milk: Preferred milk type.
        temperature: Preferred drink temperature.
        syrup: Preferred syrup.

    Returns:
        None.
    """
    with database_connection() as connection:
        connection.execute("""
            INSERT INTO preferences
                (user_id, coffee_strength, milk, temperature, syrup)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                coffee_strength = excluded.coffee_strength,
                milk = excluded.milk,
                temperature = excluded.temperature,
                syrup = excluded.syrup
        """, (
            user_id,
            coffee_strength,
            milk,
            temperature,
            syrup,
        ))


def get_preferences(user_id):
    """Retrieve the saved preferences for a user.

    Args:
        user_id: ID of the user.

    Returns:
        A dictionary of preferences, or None if no record exists.
    """
    with database_connection() as connection:
        row = connection.execute("""
            SELECT coffee_strength, milk, temperature, syrup
            FROM preferences
            WHERE user_id = ?
        """, (user_id,)).fetchone()

    if row is None:
        return None

    return {
        "coffee_strength": row[0],
        "milk": row[1],
        "temperature": row[2],
        "syrup": row[3],
    }


def save_custom_recipe(
    user_id,
    name,
    beverage,
    coffee_strength,
    milk,
    temperature,
    syrup,
):
    """Save a named custom recipe belonging to a user.

    Args:
        user_id: ID of the user saving the recipe.
        name: User-chosen recipe name.
        beverage: Base beverage.
        coffee_strength: Selected coffee strength.
        milk: Selected milk type.
        temperature: Selected temperature.
        syrup: Selected syrup.

    Returns:
        A tuple containing success status and a message.
    """
    name = name.strip()

    if not name:
        return False, "Please enter a name for your recipe."

    with database_connection() as connection:
        connection.execute("""
            INSERT INTO recipes
                (user_id, name, beverage, coffee_strength, milk,
                 temperature, syrup)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            name,
            beverage,
            coffee_strength,
            milk,
            temperature,
            syrup,
        ))

    return True, f"Recipe '{name}' saved successfully."


def get_custom_recipes(user_id):
    """Retrieve all custom recipes belonging to a specific user.

    Args:
        user_id: ID of the user.

    Returns:
        A list of dictionaries representing the user's recipes.
    """
    with database_connection() as connection:
        rows = connection.execute("""
            SELECT id, name, beverage, coffee_strength, milk,
                   temperature, syrup
            FROM recipes
            WHERE user_id = ?
            ORDER BY name COLLATE NOCASE
        """, (user_id,)).fetchall()

    columns = [
        "id",
        "name",
        "beverage",
        "coffee_strength",
        "milk",
        "temperature",
        "syrup",
    ]

    return [dict(zip(columns, row)) for row in rows]


def place_order(user_id, beverage, order_details, amount, ingredients):
    """Record a completed demo order and deduct its ingredients atomically.

    Args:
        user_id: ID of the ordering user.
        beverage: Name of the selected drink.
        order_details: Dictionary containing the selected customizations.
        amount: Price of the drink.
        ingredients: Dictionary of required ingredient quantities.

    Returns:
        A tuple containing success status and a message.
    """
    if amount < 0:
        return False, "Order amount cannot be negative."

    for ingredient, required in ingredients.items():
        if required < 0:
            return False, (
                f"Required quantity for {ingredient} cannot be negative."
            )

    with database_connection() as connection:
        # Check every ingredient before changing any stock.
        for ingredient, required in ingredients.items():
            row = connection.execute("""
                SELECT quantity, threshold
                FROM inventory
                WHERE ingredient = ?
            """, (ingredient,)).fetchone()

            if row is None:
                return False, f"{ingredient} is missing from inventory."

            quantity, threshold = row

            if quantity - required < threshold:
                return False, f"Not enough {ingredient} to place this order."

        # Deduct ingredients only after all checks pass.
        for ingredient, required in ingredients.items():
            connection.execute("""
                UPDATE inventory
                SET quantity = quantity - ?
                WHERE ingredient = ?
            """, (required, ingredient))

        # Record the demo transaction.
        connection.execute("""
            INSERT INTO transactions
                (user_id, beverage, order_details, amount,
                 payment_method, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            beverage,
            str(order_details),
            amount,
            "Demo",
            "Completed",
        ))

    return True, "Order placed successfully."


def get_user_transactions(user_id):
    """Retrieve the transaction history for a user.

    Args:
        user_id: ID of the user.

    Returns:
        A list of dictionaries containing transaction information.
    """
    with database_connection() as connection:
        rows = connection.execute("""
            SELECT id, beverage, order_details, amount,
                   payment_method, status, created_at
            FROM transactions
            WHERE user_id = ?
            ORDER BY created_at DESC, id DESC
        """, (user_id,)).fetchall()

    columns = [
        "id",
        "beverage",
        "order_details",
        "amount",
        "payment_method",
        "status",
        "created_at",
    ]

    return [dict(zip(columns, row)) for row in rows]
