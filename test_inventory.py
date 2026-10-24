
"""Automated tests for SmartBrew ingredient availability."""

import unittest
from unittest.mock import patch

from database import check_ingredient_availability


class TestInventoryAvailability(unittest.TestCase):
    """Test ingredient availability without modifying the real database."""

    @patch("database.get_inventory")
    def test_available_ingredients(self, mock_get_inventory):
        """Confirm ingredients are available when stock stays above thresholds."""
        mock_get_inventory.return_value = {
            "Coffee": {"quantity": 500, "threshold": 50},
            "Milk": {"quantity": 2000, "threshold": 200},
        }

        available, problems = check_ingredient_availability(
            {"Coffee": 20, "Milk": 100}
        )

        self.assertTrue(available)
        self.assertEqual(problems, [])

    @patch("database.get_inventory")
    def test_insufficient_coffee(self, mock_get_inventory):
        """Reject an order that would reduce coffee below its threshold."""
        mock_get_inventory.return_value = {
            "Coffee": {"quantity": 100, "threshold": 50},
        }

        available, problems = check_ingredient_availability(
            {"Coffee": 1000}
        )

        self.assertFalse(available)
        self.assertTrue(problems)

    @patch("database.get_inventory")
    def test_stock_threshold_is_enforced(self, mock_get_inventory):
        """Reject an order that would leave stock below its minimum threshold."""
        mock_get_inventory.return_value = {
            "Coffee": {"quantity": 60, "threshold": 50},
        }

        available, problems = check_ingredient_availability(
            {"Coffee": 20}
        )

        self.assertFalse(available)
        self.assertTrue(problems)


if __name__ == "__main__":
    unittest.main()
