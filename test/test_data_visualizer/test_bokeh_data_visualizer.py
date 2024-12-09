import unittest
import os
import pandas as pd
import numpy as np
from datetime import datetime
import sys
# Add the 'src' directory to the system path
sys.path.insert(0, os.path.abspath(os.path.join(
    os.path.dirname(__file__), '../../src/')))
from exception_handler import DataVisualizationError
from data_visualizer.bokeh_data_visualizer import bokeh_data_visualizer


class test_bokeh_data_visualizer(unittest.TestCase):
    """Unit tests for the bokeh_data_visualizer class"""

    def setUp(self):
        """Set up test data and class instance"""
        self.visualizer = bokeh_data_visualizer()

        # Training data
        self.x_train = np.linspace(0, 10, 100)
        # Two training functions
        self.y_train = np.vstack([self.x_train**2, self.x_train**3]).T

        # Ideal functions
        self.ideal_functions = pd.DataFrame({
            'x': self.x_train,
            'ideal_func_1': self.x_train**2 + 1,
            'ideal_func_2': self.x_train**3 + 2,
        })

        # Test data
        self.x_test = np.linspace(0, 10, 20)
        self.y_test = self.x_test**2 + 0.5

        # Mapped data
        self.mapped_data = pd.DataFrame({
            'X (test func)': self.x_test,
            'Y (test func)': self.y_test,
            'ideal_func_val': self.x_test**2 + 1,
            'Delta Y (test func)': np.abs(self.x_test**2 + 1 - self.y_test),
            'No. of ideal func': [1] * len(self.x_test)
        })

        self.current_dateTime = datetime.now().strftime("%Y%m%d%H%M%S")

        # Create output directory if not exists
        self.output_dir = "./graphs"
        os.makedirs(self.output_dir, exist_ok=True)

    def test_visualize_data_success(self):
        """Test that visualize_data runs without exceptions and creates an output file"""
        output_file_path = f"{
            self.output_dir}/graph_plotting_{self.current_dateTime}.html"

        try:
            self.visualizer.visualize_data(
                self.x_train, self.y_train, self.ideal_functions,
                self.x_test, self.y_test, self.mapped_data, self.current_dateTime
            )
        except Exception as e:
            self.fail(f"visualize_data raised an exception unexpectedly: {e}")

        # Check if output file was created
        self.assertTrue(os.path.exists(output_file_path))

    def test_visualize_data_error(self):
        """Test that visualize_data raises DataVisualizationError on invalid input"""
        with self.assertRaises(DataVisualizationError):
            self.visualizer.visualize_data(
                None, None, None, None, None, None, self.current_dateTime
            )

    def tearDown(self):
        """Clean up created files after tests"""
        output_file_path = f"{
            self.output_dir}/graph_plotting_{self.current_dateTime}.html"
        if os.path.exists(output_file_path):
            os.remove(output_file_path)


if __name__ == '__main__':
    unittest.main()
