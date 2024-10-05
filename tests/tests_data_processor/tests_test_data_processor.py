import unittest
import pandas as pd
from data_processor.test_data_processor import TestDataProcessor

class TestTestDataProcessor(unittest.TestCase):

    def test_map_to_ideal_function(self):
        test_data = pd.DataFrame({'X': [1, 2], 'Y': [4, 5]})
        ideal_funcs = pd.DataFrame({'X': [1, 2], 'I1': [4, 5], 'I2': [10, 11]})
        max_devs = pd.Series([0.1, 10.0], index=['I1', 'I2'])

        processor = TestDataProcessor(test_data)
        result = processor.map_to_ideal_function(ideal_funcs, max_devs)

        expected = pd.DataFrame({
            'X': [1, 2],
            'Y': [4, 5],
            'Delta': [0.0, 0.0],
            'Ideal Function': ['I1', 'I1']
        })

        pd.testing.assert_frame_equal(result, expected)

if __name__ == '__main__':
    unittest.main()