import unittest
import pandas as pd
from unittest.mock import patch, mock_open
from file_operations.csv_file_operations import CsvFileOperations

class TestCsvFileOperations(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data='X,Y\n1,4\n2,5\n3,6')
    def test_read(self, mock_file):
        file_ops = CsvFileOperations()
        result = file_ops.read('dummy.csv')
        expected = pd.DataFrame({'X': [1, 2, 3], 'Y': [4, 5, 6]})
        pd.testing.assert_frame_equal(result, expected)

if __name__ == '__main__':
    unittest.main()