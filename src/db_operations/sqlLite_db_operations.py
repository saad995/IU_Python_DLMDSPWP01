from sqlalchemy import create_engine, Table, Column, Float, Integer, MetaData
from sqlalchemy.orm import sessionmaker
from .db_operations import DBOperations
from exception_handler import handle_exception

class SQLiteDBOperations(DBOperations):
    """SQLite database operations using SQLAlchemy."""

    def __init__(self, db_url):
        """
        Initialize the database operations.
        :param db_url: Database URL for SQLAlchemy.
        """
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)
        self.metadata = MetaData()

    @handle_exception
    def create_table(self, table_name, column_names):
        """
        Create a table in the database based on given column names.
        :param table_name: Name of the table to create.
        :param column_names: List of column names for the table.
        """
        columns = []
        for col in column_names:
            if col.startswith("x"):
                columns.append(Column('x', Float, primary_key=True))
            elif (col.startswith("y") or col.startswith("d")):
                columns.append(Column(col, Float))
            else:
                columns.append(Column(col, Integer))
        
        table = Table(table_name, self.metadata, *columns)
        table.create(self.engine)

    @handle_exception
    def insert_data(self, table_name, data):
        """
        Insert data into a specific table.
        :param table_name: Name of the table.
        :param data: List of dictionaries containing data to insert.
        """
        table = Table(table_name, self.metadata, autoload_with=self.engine)
        with self.Session() as session:
            session.execute(table.insert(), data)
            session.commit()

    @handle_exception
    def fetch_data(self, table_name):
        """
        Fetch data from a specific table.
        :param table_name: Name of the table.
        :return: Fetched data as a list of dictionaries.
        """
        table = Table(table_name, self.metadata, autoload_with=self.engine)
        with self.Session() as session:
            result = session.execute(table.select()).fetchall()
        return [dict(row) for row in result]