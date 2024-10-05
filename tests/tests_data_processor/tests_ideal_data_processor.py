import unittest
import pandas as pd
from data_processor.ideal_data_processor import IdealDataProcessor
from exception_handler import DataProcessingError

class TestIdealDataProcessor(unittest.TestCase):
    """Unit tests for IdealDataProcessor class"""

    def setUp(self):
        """Set up test data"""
        self.processor = IdealDataProcessor()
        self.train_data = pd.DataFrame({
            'x': [1, 2, 3],
            'y1': [1.1, 2.1, 3.0],
            'y2': [1.2, 2.2, 2.9],
            'y3': [1.0, 2.0, 3.1],
            'y4': [1.1, 2.0, 3.2]
        })
        self.ideal_data = pd.DataFrame({
            'x': [1, 2, 3],
            'y1': [1.1, 2.1, 3.0],
            'y2': [1.2, 2.2, 3.1],
            'y3': [1.0, 2.0, 3.2],
            'y4': [1.2, 2.1, 3.1]
        })

    def test_find_best_fit(self):
        """Test finding the best fit ideal functions"""
        best_fit = self.processor.find_best_fit(self.train_data, self.ideal_data)
        expected_best_fit = [
            min(
                [(self.train_data[['y1', 'y2', 'y3', 'y4']].iloc[0] - ideal).pow(2).sum() for ideal in self.ideal_data[['y1', 'y2', 'y3', 'y4']].values]
            ),
            min(
                [(self.train_data[['y1', 'y2', 'y3', 'y4']].iloc[1] - ideal).pow(2).sum() for ideal in self.ideal_data[['y1', 'y2', 'y3', 'y4']].values]
            ),
            min(
                [(self.train_data[['y1', 'y2', 'y3', 'y4']].iloc[2] - ideal).pow(2).sum() for ideal in self.ideal_data[['y1', 'y2', 'y3', 'y4']].values]
            )
        ]
        self.assertAlmostEqual(best_fit[0], expected_best_fit[0])
        self.assertAlmostEqual(best_fit[1], expected_best_fit[1])
        self.assertAlmostEqual(best_fit[2], expected_best_fit[2])

    def test_find_best_fit_empty_data(self):
        """Test finding best fit with empty data"""
        processor = IdealDataProcessor()
        empty_train_data = pd.DataFrame(columns=['x', 'y1', 'y2', 'y3', 'y4'])
        empty_ideal_data = pd.DataFrame(columns=['x', 'y1', 'y2', 'y3', 'y4'])
        with self.assertRaises(Exception):
            processor.find_best_fit(empty_train_data, empty_ideal_data)

if __name__ == '__main__':
    unittest.main()