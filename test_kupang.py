import unittest
from unittest.mock import patch, mock_open, MagicMock
from kupang import ShoppingMall, Order


class TestShoppingMall(unittest.TestCase):

    def setUp(self):
        # Initialize the ShoppingMall class
        self.shopping_mall = ShoppingMall()

    @patch("builtins.open", new_callable=mock_open)
    def test_load_items(self, mock_file):
        # Mock product data
        mock_file.return_value.read.return_value = "PROD1234,Item1,1000,10\nPROD5678,Item2,500,20\n"
        
        # Call load_items and verify products are loaded correctly
        self.shopping_mall.load_items()
        self.assertIn("PROD1234", self.shopping_mall.products)
        self.assertEqual(self.shopping_mall.products["PROD1234"], ("Item1", 1000, 10))

    @patch("builtins.open", new_callable=mock_open)
    def test_save_items(self, mock_file):
        # Add products to save
        self.shopping_mall.products = {
            "PROD1234": ("Item1", 1000, 10),
            "PROD5678": ("Item2", 500, 20),
        }
        self.shopping_mall.save_items()

        # Check saved content
        mock_file().write.assert_any_call("PROD1234,Item1,1000,10\n")
        mock_file().write.assert_any_call("PROD5678,Item2,500,20\n")

    @patch("builtins.open", new_callable=mock_open)
    def test_load_orders(self, mock_file):
        # Mock order data
        mock_file.return_value.read.return_value = "ORD0001,PROD1234,Item1,1000,2,010-1234-5678,2024-11-28\n"

        self.shopping_mall.load_orders()

        # Verify orders are loaded correctly
        self.assertEqual(len(self.shopping_mall.orders), 1)
        order = self.shopping_mall.orders[0]
        self.assertEqual(order.order_id, "ORD0001")
        self.assertEqual(order.product_name, "Item1")

    @patch("builtins.input", side_effect=["Item1", "1000", "10"])
    @patch("builtins.open", new_callable=mock_open)
    def test_add_product(self, mock_file, mock_input):
        # Call add_product and verify the addition
        with patch.object(self.shopping_mall, "check_id", return_value=True):
            self.shopping_mall.add_product()

        # Verify products were updated
        self.assertIn("PROD", next(iter(self.shopping_mall.products)))

    @patch("builtins.input", side_effect=["PROD1234", "2", "0"])
    def test_add_order(self, mock_input):
        # Mock products
        self.shopping_mall.products = {"PROD1234": ("Item1", 1000, 10)}
        self.shopping_mall.orders = [
            Order("ORD0001", "PROD1234", "Item1", 1000, 2, "010-1234-5678", "2024-11-28")
        ]

        with patch.object(self.shopping_mall, "check_id", return_value=True):
            self.shopping_mall.add_order()

        # Verify order addition
        self.assertEqual(len(self.shopping_mall.orders), 1)
        order = self.shopping_mall.orders[0]
        self.assertEqual(order.product_name, "Item1")
        self.assertEqual(order.quantity, 2)

    @patch("builtins.input", side_effect=["ORD0001", "1"])
    def test_return_product(self, mock_input):
        # Mock products and orders
        self.shopping_mall.products = {"PROD1234": ("Item1", 1000, 10)}
        self.shopping_mall.orders = [
            Order("ORD0001", "PROD1234", "Item1", 1000, 2, "010-1234-5678", "2024-11-28")
        ]
        self.shopping_mall.current_user = {"phone": "010-1234-5678", "order_date": "2024-11-29"}

        with patch("builtins.open", mock_open()) as mock_file:
            self.shopping_mall.return_product()

        # Verify inventory update
        self.assertEqual(self.shopping_mall.products["PROD1234"][2], 11)

    @patch("builtins.input", side_effect=["0"])
    def test_role_selection_exit(self, mock_input):
        # Test exiting the program
        with self.assertRaises(SystemExit):
            self.shopping_mall.role_selection()


if __name__ == "__main__":
    unittest.main()
