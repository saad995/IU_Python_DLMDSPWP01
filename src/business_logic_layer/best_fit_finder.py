import numpy as np
import pandas as pd
import csv
from exception_handler import DataProcessingError


class best_fit_finder:
    """
    Business logic class for data processing.
    This class defines the functions needed to find the best fit functions, calculate maximum deviations and map the best fit functions to the test data.
    """

    def __init__(self, train_data, ideal_data):
        self.train_data = train_data
        self.ideal_data = ideal_data
        self.best_fit_functions = None
        self.max_deviations = []
        self.test_dataframe = None
        self.mapped_dataframe = None

    def find_best_fit_functions(self):
        """
        Finds the best fit functions for the training dataset against the ideal functions loaded in the class using the sum of squared differences (Least-Square) technique.
        """
        try:
            best_fit = []
            best_fit.append(self.train_data['x'])
            # Iterate over each y column in the training data
            for col_train in self.train_data.columns[1:]:
                min_diff = np.inf
                best_func = None
                y_train = self.train_data[col_train]
                # Iterate over each ideal y column
                for col_ideal in self.ideal_data.columns[1:]:
                    y_ideal = self.ideal_data[col_ideal]
                    # Calculate sum of squared differences
                    squared_diff = ((y_train - y_ideal) ** 2).sum()
                    if squared_diff < min_diff:
                        min_diff = squared_diff
                        best_func = y_ideal
                best_fit.append(best_func)
            # Concatenate the best fit functions as a DataFrame
            self.best_fit_functions = pd.concat(best_fit, axis=1)
        except Exception as e:
            raise DataProcessingError(
                f"Error in finding best fit functions: {str(e)}")

    def calculate_max_deviations(self):
        """
        Calculates maximum deviation between training dataset and the best fit functions.
        """
        try:
            for col_train, col_ideal in zip(self.train_data.columns[1:], self.best_fit_functions.columns[1:]):
                y_train = self.train_data[col_train]
                y_ideal = self.best_fit_functions[col_ideal]
                max_deviation = abs(y_train - y_ideal).max()
                self.max_deviations.append(max_deviation * np.sqrt(2))
        except Exception as e:
            raise DataProcessingError(
                f"Error in calculating maximum deviations: {str(e)}")

    def map_test_data(self, file_path):
        """
        Function to map test data to the best fit ideal functions.
        Test data parsed line by line is captured in the property of this class named 'test_dataframe'.
        Mapping added against this test data is captured in the property of this class named 'mapped_dataframe'.
        :param file_path: File path as string.
        """
        try:
            test_data = []
            mapped_data = []
            with open(file_path, mode="r") as file:  # Iterate over each row in the test data
                reader = csv.reader(file)
                next(reader)  # Skip the header row if necessary.
                for row in reader:
                    x_test, y_test = float(row[0]), float(row[1])
                    test_data.append((x_test, y_test))
                    min_deviation = np.inf
                    best_fit_func = None
                    best_deviation = None
                    best_deviation_no_of_ideal_func = None
                    for i, col_ideal in enumerate(self.best_fit_functions.columns[1:]):
                        y_ideal_value = self.best_fit_functions.loc[self.best_fit_functions['x']
                                                                    == x_test, col_ideal].values[0]
                        deviation = abs(y_test - y_ideal_value)
                        if deviation < min_deviation and deviation <= self.max_deviations[i]:
                            min_deviation = deviation
                            best_fit_func = i + 1  # Indicate which of the four ideal functions it corresponds to
                            best_deviation = deviation
                            best_deviation_no_of_ideal_func = col_ideal.removeprefix(
                                'y')
                    if best_fit_func is not None:
                        mapped_data.append((
                            x_test,
                            y_test,
                            best_deviation,
                            best_deviation_no_of_ideal_func,
                            y_ideal_value
                        ))
            self.test_dataframe = pd.DataFrame(
                test_data,
                columns=['x', 'y']
            )
            self.mapped_dataframe = pd.DataFrame(
                mapped_data,
                columns=[
                    'X (test func)',
                    'Y (test func)',
                    'Delta Y (test func)',
                    'No.  of ideal func',
                    'ideal_func_val'
                ]
            )
        except Exception as e:
            raise DataProcessingError(
                f"Error in mapping test data to best fit functions: {str(e)}")
