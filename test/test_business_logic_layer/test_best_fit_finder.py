import unittest
import pandas as pd
import os
from io import StringIO
import sys
# Add the 'src' directory to the system path
sys.path.insert(0, os.path.abspath(os.path.join(
    os.path.dirname(__file__), '../../src/')))
from business_logic_layer.best_fit_finder import best_fit_finder
from exception_handler import DataProcessingError


class test_best_fit_finder(unittest.TestCase):
    def setUp(self):
        """
        Sets up the test data for training and ideal datasets.
        """
        # Sample training and ideal data
        train_data_csv = """x,y1,y2
                            1,10,20
                            2,15,25
                            3,20,30
                            4,25,35"""
        ideal_data_csv = """x,y1,y2
                            1,10.1,20.1
                            2,14.8,24.9
                            3,19.9,30.2
                            4,25.1,35.0"""

        self.train_data = pd.read_csv(StringIO(train_data_csv))
        self.ideal_data = pd.read_csv(StringIO(ideal_data_csv))
        self.test_file_path = "test_data.csv"

        self.best_fit_finder = best_fit_finder(
            self.train_data, self.ideal_data)

    def tearDown(self):
        """
        Cleanup test files after execution.
        """
        if os.path.exists(self.test_file_path):
            os.remove(self.test_file_path)

    def test_find_best_fit_functions(self):
        """
        Test the functionality of finding the best fit functions.
        """
        self.best_fit_finder.find_best_fit_functions()
        # Check if the best fit functions were calculated correctly
        self.assertIsNotNone(self.best_fit_finder.best_fit_functions)
        self.assertEqual(
            len(self.best_fit_finder.best_fit_functions.columns), 3)

    def test_calculate_max_deviations(self):
        """
        Test the calculation of maximum deviations.
        """
        self.best_fit_finder.find_best_fit_functions()
        self.best_fit_finder.calculate_max_deviations()
        # Check if max deviations were calculated
        self.assertEqual(len(self.best_fit_finder.max_deviations), 2)
        self.assertGreater(self.best_fit_finder.max_deviations[0], 0)

    def test_map_test_data_success(self):
        """
        Test mapping test data to best fit functions successfully.
        """
        # Create a temporary test data file
        test_data_csv = """x,y
                        1,10.1
                        2,15.2
                        3,20.1
                        4,25.0"""
        with open(self.test_file_path, "w") as file:
            file.write(test_data_csv)

        self.best_fit_finder.find_best_fit_functions()
        self.best_fit_finder.calculate_max_deviations()
        self.best_fit_finder.map_test_data(self.test_file_path)

        # Check if test data and mapped data are populated
        self.assertIsNotNone(self.best_fit_finder.test_dataframe)
        self.assertIsNotNone(self.best_fit_finder.mapped_dataframe)

        # Validate structure of mapped data
        expected_columns = [
            'X (test func)',
            'Y (test func)',
            'Delta Y (test func)',
            'No.  of ideal func',
            'ideal_func_val'
        ]
        self.assertListEqual(
            list(self.best_fit_finder.mapped_dataframe.columns),
            expected_columns
        )

    def test_map_test_data_no_mapping(self):
        """
        Test mapping test data where no mapping should occur due to large deviations.
        """
        # Create test data with large deviations
        test_data_csv = """x,y
                        1,50
                        2,60
                        3,70
                        4,80"""
        with open(self.test_file_path, "w") as file:
            file.write(test_data_csv)

        self.best_fit_finder.find_best_fit_functions()
        self.best_fit_finder.calculate_max_deviations()
        self.best_fit_finder.map_test_data(self.test_file_path)

        # Check if mapped dataframe is empty
        self.assertTrue(self.best_fit_finder.mapped_dataframe.empty)

    def test_find_best_fit_functions_error(self):
        """
        Test error handling in finding the best fit functions.
        """
        self.best_fit_finder.train_data = None  # Corrupt the training data
        with self.assertRaises(DataProcessingError):
            self.best_fit_finder.find_best_fit_functions()

    def test_calculate_max_deviations_error(self):
        """
        Test error handling in calculating maximum deviations.
        """
        self.best_fit_finder.best_fit_functions = None  # Corrupt the best fit functions
        with self.assertRaises(DataProcessingError):
            self.best_fit_finder.calculate_max_deviations()

    def test_map_test_data_error(self):
        """
        Test error handling in mapping test data.
        """
        invalid_file_path = "invalid_test_data.csv"
        with self.assertRaises(DataProcessingError):
            self.best_fit_finder.map_test_data(invalid_file_path)


if __name__ == "__main__":
    unittest.main()
