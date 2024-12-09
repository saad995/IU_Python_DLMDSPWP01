import os
import pandas as pd
import unittest
from unittest.mock import patch
import sys
# Add the 'src' directory to the system path
sys.path.insert(0, os.path.abspath(os.path.join(
    os.path.dirname(__file__), '../../src/')))
from file_operations.csv_file_operations import csv_file_operations
from exception_handler import DataProcessingError


class test_csv_file_operations(unittest.TestCase):
    def setUp(self):
        """Setup resources before each test."""
        self.csv_operations = csv_file_operations()
        self.test_csv_content = "col1,col2,col3\n1,2,3\n4,5,6\n7,8,9"
        self.test_csv_path = "test.csv"

    def tearDown(self):
        """Cleanup resources after each test."""
        if os.path.exists(self.test_csv_path):
            os.remove(self.test_csv_path)

    def test_read_file_success(self):
        """Test reading a CSV file successfully."""
        # Write test CSV content to a temporary file
        with open(self.test_csv_path, "w") as file:
            file.write(self.test_csv_content)

        # Read the file using the csv_file_operations class
        df = self.csv_operations.read_file(self.test_csv_path)
        expected_df = pd.DataFrame({
            "col1": [1, 4, 7],
            "col2": [2, 5, 8],
            "col3": [3, 6, 9]
        })

        # Assert the content matches
        pd.testing.assert_frame_equal(df, expected_df)

    def test_read_file_non_existent(self):
        """Test handling of non-existent file."""
        non_existent_file_path = "non_existent.csv"
        with self.assertRaises(DataProcessingError) as context:
            self.csv_operations.read_file(non_existent_file_path)
        self.assertIn("Error processing CSV file", str(context.exception))

    @patch("pandas.read_csv")
    def test_read_file_pandas_error(self, mock_read_csv):
        """Test handling of pandas read_csv errors."""
        mock_read_csv.side_effect = ValueError("Mocked pandas error")

        with self.assertRaises(DataProcessingError) as context:
            self.csv_operations.read_file(self.test_csv_path)
        self.assertIn("Mocked pandas error", str(context.exception))

    def test_read_file_empty_file(self):
        """Test reading an empty CSV file."""
        # Create an empty CSV file
        with open(self.test_csv_path, "w") as file:
            file.write("")

        with self.assertRaises(DataProcessingError) as context:
            self.csv_operations.read_file(self.test_csv_path)
        self.assertIn("No columns to parse from file", str(context.exception))


if __name__ == "__main__":
    unittest.main()