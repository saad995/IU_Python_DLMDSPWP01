import unittest
import pandas as pd
from db_operations.sqlLite_db_operations import SqlLiteDbOperations

class TestSqlLiteDbOperations(unittest.TestCase):

    def test_insert_data(self):
        db_ops = SqlLiteDbOperations()
        connection = db_ops.connect(':memory:')
        data = pd.DataFrame({'X': [1, 2, 3], 'Y': [4, 5, 6]})

        db_ops.insert_data('test_table', data)

        result = pd.read_sql('SELECT * FROM test_table', connection)
        pd.testing.assert_frame_equal(result, data)

if __name__ == '__main__':
    unittest.main()