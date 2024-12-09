from abc import ABC, abstractmethod


class db_operations(ABC):
    """
    Abstract base class for database operations.
    This class defines the interface that all derived database operation classes must implement.
    """

    @abstractmethod
    def create_table(self, table_name, column_names):
        """
        Create a table in the database.
        :param table_name: Name of the table to create.
        :param column_names: List of column names for the table.
        """
        pass

    @abstractmethod
    def insert_data(self, table_name, data):
        """
        Insert data into a specific table.
        :param table_name: Name of the table.
        :param data: List of dictionaries containing data to insert.
        """
        pass

    @abstractmethod
    def fetch_data(self, table_name):
        """
        Fetch data from a specific table.
        :param table_name: Name of the table.
        :return: Fetched data as a list of dictionaries.
        """
        pass
