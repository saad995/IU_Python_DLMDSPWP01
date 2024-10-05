from data_processor.data_processor import DataProcessor
from exception_handler import DataProcessingError
import numpy as np

class TestDataProcessor(DataProcessor):
    """Derived class for test data processing"""

    def map_test_data(self, test_data, ideal_functions, train_data, best_fit_indices):
        """Maps test data to ideal functions"""
        try:
            mapped_data = []
            for i in range(test_data.shape[1]):  # For each test function
                test_func = test_data[:, i]
                for idx, best_fit in enumerate(best_fit_indices):
                    ideal_func = ideal_functions[:, best_fit]
                    deviation = np.max(np.abs(test_func - ideal_func))
                    max_deviation = np.max(np.abs(train_data[:, idx] - ideal_func))
                    if deviation <= max_deviation * np.sqrt(2):
                        mapped_data.append((test_func, ideal_func, deviation, best_fit))
            return mapped_data
        except Exception as e:
            raise DataProcessingError(f"Error mapping test data: {str(e)}")