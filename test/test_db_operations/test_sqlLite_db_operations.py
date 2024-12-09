import unittest
import tempfile
import os
from sqlalchemy import inspect
import sys
# Add the 'src' directory to the system path
sys.path.insert(0, os.path.abspath(os.path.join(
    os.path.dirname(__file__), '../../src/')))
from exception_handler import DatabaseError
from db_operations.sqlLite_db_operations import sqlLite_db_operations


class test_sqlLite_db_operations(unittest.TestCase):
    """Unit tests for sqlLite_db_operations class."""

    def setUp(self):
        """Set up a temporary SQLite database."""
        self.db_fd, self.db_path = tempfile.mkstemp(suffix=".db")
        self.db_url = f"sqlite:///{self.db_path}"
        self.db_ops = sqlLite_db_operations(self.db_url)

    def tearDown(self):
        """Remove the temporary SQLite database."""
        try:
            # Close the engine to release the SQLite file
            self.db_ops.engine.dispose()
            os.close(self.db_fd)
            os.unlink(self.db_path)
        except Exception as e:
            raise Exception(
                f"Error occurred in tear down of db operation tests: {e}")

    def test_create_table(self):
        """Test creating a table in the database."""
        table_name = "test_table"
        columns = ["x", "y", "delta", "ideal_function"]

        # Test table creation
        try:
            self.db_ops.create_table(table_name, columns)
        except DatabaseError as e:
            self.fail(f"create_table raised an exception: {e}")

        # Verify table existence
        inspector = inspect(self.db_ops.engine)
        self.assertIn(table_name, inspector.get_table_names(),
                      "Table was not created successfully")

    def test_insert_and_fetch_data(self):
        """Test inserting and fetching data."""
        table_name = "test_table"
        column_names = ["x", "y"]
        self.db_ops.create_table(table_name, column_names)

        # Insert data (ensure it's a list of dictionaries)
        data = [
            {"x": 1.0, "y": 2.0},
            {"x": 2.0, "y": 3.5}
        ]
        try:
            self.db_ops.insert_data(table_name, data)
        except DatabaseError as e:
            self.fail(f"insert_data raised an exception: {e}")

        # Fetch data
        try:
            fetched_data = self.db_ops.fetch_data(table_name)
        except DatabaseError as e:
            self.fail(f"fetch_data raised an exception: {e}")

        # Check that the fetched data matches the inserted data
        self.assertEqual(len(fetched_data), len(data))
        self.assertEqual(fetched_data, data)

    def test_insert_data_with_invalid_table(self):
        """Test inserting data into a non-existent table."""
        table_name = "non_existent_table"
        data = [{"x": 1.0, "y": 2.0}]
        with self.assertRaises(DatabaseError):
            self.db_ops.insert_data(table_name, data)

    def test_fetch_data_with_invalid_table(self):
        """Test fetching data from a non-existent table."""
        table_name = "non_existent_table"
        with self.assertRaises(DatabaseError):
            self.db_ops.fetch_data(table_name)


if __name__ == "__main__":
    unittest.main()
