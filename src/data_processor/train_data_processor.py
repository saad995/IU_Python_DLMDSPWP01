from exception_handler import DataProcessingError
from data_processor.data_processor import DataProcessor
import pandas as pd

class TrainDataProcessor(DataProcessor):
    """Derived class for training data processing"""

    def process_training_data(self, train_data, ideal_data):
        """
        Processes training data and finds the best fit ideal functions.
        :param train_data: DataFrame containing the training data.
        :param ideal_data: DataFrame containing the ideal functions data.
        :return: List of indices of the best fit ideal functions for each training function.
        """
        try:
            # Initialize a list to store the best fit indices
            best_fit_indices = []

            # Iterate over each row in the training data
            for index, row in train_data.iterrows():
                # Extract the x-values for this training function
                x_train = row.index
                y_train = row.values

                # Initialize a list to store the squared differences for each ideal function
                squared_differences = []

                # Iterate over each ideal function
                for _, ideal_row in ideal_data.iterrows():
                    # Extract the y-values for this ideal function
                    y_ideal = ideal_row.values

                    # Compute the squared differences
                    squared_diff = ((y_train - y_ideal) ** 2).sum()
                    squared_differences.append(squared_diff)

                # Find the index of the ideal function with the minimum squared difference
                best_fit_index = squared_differences.index(min(squared_differences))
                best_fit_indices.append(best_fit_index)

            return best_fit_indices
        except Exception as e:
            raise DataProcessingError(f"Error processing training data: {str(e)}")