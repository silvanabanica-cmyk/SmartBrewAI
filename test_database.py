
"""Unit tests for SmartBrew AI database functions."""

import os
import sqlite3
import tempfile
import unittest
from unittest.mock import patch

import database


class TestDatabase(unittest.TestCase):
    """Test database operations using an isolated temporary database."""

    def setUp(self):
        """Create a temporary database and track all opened connections."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(
            self.temp_dir.name,
            "test_smartbrew.db",
        )
        self.connections = []

        self.database_name_patcher = patch.object(
            database,
            "DATABASE_NAME",
            self.db_path,
        )
        self.connection_patcher = patch.object(
            database,
            "get_connection",
            self.get_test_connection,
        )

        self.database_name_patcher.start()
        self.connection_patcher.start()

        database.initialize_database()
        database.seed_inventory()

    def get_test_connection(self):
        """Open and track a connection so it can be closed after a test."""
        connection = sqlite3.connect(self.db_path)
        self.connections.append(connection)
        return connection

    def tearDown(self):
        """Close database connections before deleting the temporary folder."""
        for connection in self.connections:
            try:
                connection.close()
            except sqlite3.Error:
                pass

        self.connection_patcher.stop()
        self.database_name_patcher.stop()
        self.temp_dir.cleanup()

    def create_test_user(self, username="testuser"):
        """Create a user and return its database ID."""
        connection = sqlite3.connect(self.db_path)

        try:
            cursor = connection.execute(
                """
                INSERT INTO users (username, password_hash)
                VALUES (?, ?)
                """,
                (username, "test_hash"),
            )
            connection.commit()
            return cursor.lastrowid
        finally:
            connection.close()

    # Inventory tests

    def test_seed_inventory_creates_default_ingredients(self):
        """Verify that seeding creates the four default ingredients."""
        inventory = database.get_inventory()

        self.assertEqual(len(inventory), 4)
        self.assertEqual(
            inventory["Coffee"],
            {"quantity": 500, "threshold": 50},
        )
        self.assertEqual(
            inventory["Water"],
            {"quantity": 5000, "threshold": 500},
        )
        self.assertEqual(
            inventory["Milk"],
            {"quantity": 2000, "threshold": 200},
        )
        self.assertEqual(
            inventory["Chocolate"],
            {"quantity": 500, "threshold": 50},
        )

    def test_seed_inventory_does_not_overwrite_existing_stock(self):
        """Verify that running the seeding function twice preserves stock."""
        database.refill_inventory("Coffee", 25)

        database.seed_inventory()

        inventory = database.get_inventory()
        self.assertEqual(inventory["Coffee"]["quantity"], 525)

    def test_refill_inventory_increases_stock(self):
        """Verify that a valid refill increases the ingredient quantity."""
        before = database.get_inventory()["Coffee"]["quantity"]

        success, message = database.refill_inventory("Coffee", 20)

        after = database.get_inventory()["Coffee"]["quantity"]

        self.assertTrue(success)
        self.assertIn("Added", message)
        self.assertEqual(after, before + 20)

    def test_refill_inventory_rejects_zero_quantity(self):
        """Verify that a refill of zero units is rejected."""
        before = database.get_inventory()["Coffee"]["quantity"]

        success, message = database.refill_inventory("Coffee", 0)

        after = database.get_inventory()["Coffee"]["quantity"]

        self.assertFalse(success)
        self.assertIn("greater than zero", message)
        self.assertEqual(after, before)

    def test_refill_inventory_rejects_negative_quantity(self):
        """Verify that a refill with a negative quantity is rejected."""
        before = database.get_inventory()["Coffee"]["quantity"]

        success, message = database.refill_inventory("Coffee", -5)

        after = database.get_inventory()["Coffee"]["quantity"]

        self.assertFalse(success)
        self.assertEqual(after, before)

    def test_refill_inventory_rejects_unknown_ingredient(self):
        """Verify that an ingredient absent from inventory cannot be refilled."""
        success, message = database.refill_inventory("Tea", 10)

        self.assertFalse(success)
        self.assertIn("not found", message)

    # Waste-log tests

    def test_log_waste_deducts_stock_and_records_waste(self):
        """Verify that logged waste reduces stock and creates a waste record."""
        before = database.get_inventory()["Coffee"]["quantity"]

        success, message = database.log_waste("Coffee", 10)

        after = database.get_inventory()["Coffee"]["quantity"]
        logs = database.get_waste_logs()

        self.assertTrue(success)
        self.assertIn("Recorded", message)
        self.assertEqual(after, before - 10)
        self.assertEqual(len(logs), 1)
        self.assertEqual(logs[0]["waste_type"], "Coffee")
        self.assertEqual(logs[0]["quantity"], 10)

    def test_log_waste_rejects_zero_quantity(self):
        """Verify that logging zero units of waste is rejected."""
        before = database.get_inventory()["Coffee"]["quantity"]

        success, message = database.log_waste("Coffee", 0)

        self.assertFalse(success)
        self.assertIn("greater than zero", message)
        self.assertEqual(
            database.get_inventory()["Coffee"]["quantity"],
            before,
        )
        self.assertEqual(database.get_waste_logs(), [])

    def test_log_waste_rejects_more_than_available_stock(self):
        """Verify that waste cannot exceed the available ingredient stock."""
        before = database.get_inventory()["Coffee"]["quantity"]

        success, message = database.log_waste("Coffee", before + 1)

        self.assertFalse(success)
        self.assertIn("cannot exceed", message)
        self.assertEqual(
            database.get_inventory()["Coffee"]["quantity"],
            before,
        )
        self.assertEqual(database.get_waste_logs(), [])

    def test_log_waste_rejects_unknown_ingredient(self):
        """Verify that waste cannot be logged for an unknown ingredient."""
        success, message = database.log_waste("Tea", 5)

        self.assertFalse(success)
        self.assertIn("not found", message)
        self.assertEqual(database.get_waste_logs(), [])

    # Ingredient-availability tests

    def test_check_availability_accepts_sufficient_stock(self):
        """Verify that an order is available when stock stays above threshold."""
        available, problems = database.check_ingredient_availability(
            {"Coffee": 10, "Water": 100}
        )

        self.assertTrue(available)
        self.assertEqual(problems, [])

    def test_check_availability_rejects_stock_below_threshold(self):
        """Verify that an order breaching the minimum stock is rejected."""
        available, problems = database.check_ingredient_availability(
            {"Coffee": 451}
        )

        self.assertFalse(available)
        self.assertTrue(problems)
        self.assertTrue(
            any("minimum stock" in problem for problem in problems)
        )

    def test_check_availability_rejects_unknown_ingredient(self):
        """Verify that an ingredient missing from inventory is reported."""
        available, problems = database.check_ingredient_availability(
            {"Tea": 1}
        )

        self.assertFalse(available)
        self.assertIn("Tea is missing from inventory.", problems)

    # Preference tests

    def test_get_preferences_returns_none_before_preferences_are_saved(self):
        """Verify that a new user without preferences receives None."""
        user_id = self.create_test_user()

        self.assertIsNone(database.get_preferences(user_id))

    def test_save_and_get_preferences(self):
        """Verify that a user's drink preferences can be saved and retrieved."""
        user_id = self.create_test_user()

        database.save_preferences(
            user_id,
            "Strong",
            "Oat",
            "Cold",
            "Vanilla",
        )

        preferences = database.get_preferences(user_id)

        self.assertEqual(
            preferences,
            {
                "coffee_strength": "Strong",
                "milk": "Oat",
                "temperature": "Cold",
                "syrup": "Vanilla",
            },
        )

    def test_save_preferences_updates_existing_preferences(self):
        """Verify that saving preferences again updates the existing record."""
        user_id = self.create_test_user()

        database.save_preferences(
            user_id,
            "Medium",
            "Regular",
            "Hot",
            "None",
        )
        database.save_preferences(
            user_id,
            "Strong",
            "Oat",
            "Cold",
            "Caramel",
        )

        preferences = database.get_preferences(user_id)

        self.assertEqual(preferences["coffee_strength"], "Strong")
        self.assertEqual(preferences["milk"], "Oat")
        self.assertEqual(preferences["temperature"], "Cold")
        self.assertEqual(preferences["syrup"], "Caramel")

    # Custom-recipe tests

    def test_save_and_get_custom_recipe(self):
        """Verify that a custom recipe is saved and returned for its owner."""
        user_id = self.create_test_user()

        success, message = database.save_custom_recipe(
            user_id,
            "My Latte",
            "Latte",
            "Strong",
            "Oat",
            "Hot",
            "Vanilla",
        )

        recipes = database.get_custom_recipes(user_id)

        self.assertTrue(success)
        self.assertIn("My Latte", message)
        self.assertEqual(len(recipes), 1)
        self.assertEqual(recipes[0]["name"], "My Latte")
        self.assertEqual(recipes[0]["beverage"], "Latte")
        self.assertEqual(recipes[0]["coffee_strength"], "Strong")
        self.assertEqual(recipes[0]["milk"], "Oat")
        self.assertEqual(recipes[0]["temperature"], "Hot")
        self.assertEqual(recipes[0]["syrup"], "Vanilla")

    def test_save_custom_recipe_rejects_blank_name(self):
        """Verify that a recipe with a blank name is rejected."""
        user_id = self.create_test_user()

        success, message = database.save_custom_recipe(
            user_id,
            "   ",
            "Latte",
            "Medium",
            "Regular",
            "Hot",
            "None",
        )

        self.assertFalse(success)
        self.assertIn("enter a name", message)
        self.assertEqual(database.get_custom_recipes(user_id), [])

    def test_custom_recipes_are_isolated_by_user(self):
        """Verify that users can retrieve only their own custom recipes."""
        first_user = self.create_test_user("first_user")
        second_user = self.create_test_user("second_user")

        database.save_custom_recipe(
            first_user,
            "First Recipe",
            "Latte",
            "Medium",
            "Regular",
            "Hot",
            "None",
        )
        database.save_custom_recipe(
            second_user,
            "Second Recipe",
            "Cappuccino",
            "Strong",
            "Oat",
            "Hot",
            "Vanilla",
        )

        first_recipes = database.get_custom_recipes(first_user)
        second_recipes = database.get_custom_recipes(second_user)

        self.assertEqual(
            [recipe["name"] for recipe in first_recipes],
            ["First Recipe"],
        )
        self.assertEqual(
            [recipe["name"] for recipe in second_recipes],
            ["Second Recipe"],
        )

    # Order and transaction tests

    def test_place_order_deducts_stock_and_records_transaction(self):
        """Verify that a valid order deducts stock and records a transaction."""
        user_id = self.create_test_user()
        before = database.get_inventory()

        success, message = database.place_order(
            user_id,
            "Latte",
            {"milk": "Regular", "temperature": "Hot"},
            35.0,
            {"Coffee": 10, "Milk": 100, "Water": 150},
        )

        after = database.get_inventory()
        transactions = database.get_user_transactions(user_id)

        self.assertTrue(success)
        self.assertEqual(message, "Order placed successfully.")
        self.assertEqual(
            after["Coffee"]["quantity"],
            before["Coffee"]["quantity"] - 10,
        )
        self.assertEqual(
            after["Milk"]["quantity"],
            before["Milk"]["quantity"] - 100,
        )
        self.assertEqual(
            after["Water"]["quantity"],
            before["Water"]["quantity"] - 150,
        )
        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0]["beverage"], "Latte")
        self.assertEqual(transactions[0]["amount"], 35.0)
        self.assertEqual(transactions[0]["payment_method"], "Demo")
        self.assertEqual(transactions[0]["status"], "Completed")

    def test_place_order_rejects_order_below_threshold(self):
        """Verify that an order is rejected if it breaches stock thresholds."""
        user_id = self.create_test_user()
        before = database.get_inventory()

        success, message = database.place_order(
            user_id,
            "Large Coffee",
            {},
            40.0,
            {"Coffee": 451},
        )

        after = database.get_inventory()

        self.assertFalse(success)
        self.assertIn("Not enough Coffee", message)
        self.assertEqual(after, before)
        self.assertEqual(database.get_user_transactions(user_id), [])

    def test_place_order_rejects_unknown_ingredient(self):
        """Verify that an order using an unknown ingredient is rejected."""
        user_id = self.create_test_user()
        before = database.get_inventory()

        success, message = database.place_order(
            user_id,
            "Tea",
            {},
            20.0,
            {"Tea": 10},
        )

        self.assertFalse(success)
        self.assertIn("Tea is missing from inventory", message)
        self.assertEqual(database.get_inventory(), before)
        self.assertEqual(database.get_user_transactions(user_id), [])

    def test_transactions_are_isolated_by_user(self):
        """Verify that each user sees only their own transaction history."""
        first_user = self.create_test_user("first_user")
        second_user = self.create_test_user("second_user")

        success, _ = database.place_order(
            first_user,
            "Coffee",
            {"temperature": "Hot"},
            25.0,
            {"Coffee": 10},
        )
        self.assertTrue(success)

        success, _ = database.place_order(
            second_user,
            "Latte",
            {"temperature": "Hot"},
            35.0,
            {"Milk": 100},
        )
        self.assertTrue(success)

        first_transactions = database.get_user_transactions(first_user)
        second_transactions = database.get_user_transactions(second_user)

        self.assertEqual(len(first_transactions), 1)
        self.assertEqual(first_transactions[0]["beverage"], "Coffee")

        self.assertEqual(len(second_transactions), 1)
        self.assertEqual(second_transactions[0]["beverage"], "Latte")


if __name__ == "__main__":
    unittest.main()
