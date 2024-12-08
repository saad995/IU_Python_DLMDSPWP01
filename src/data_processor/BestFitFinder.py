import numpy as np
import pandas as pd
import csv

class BestFitFinder:
    def __init__(self, train_data, ideal_data):
        self.train_data = train_data
        self.ideal_data = ideal_data

    # def find_best_fit_functions(self):
    #     best_fit_functions = {}
        
    #     for train_col in self.train_data.columns[1:]:  # Skip the first column (x values)
    #         best_fit = None
    #         min_squared_diff = float('inf')
            
    #         for ideal_col in self.ideal_data.columns[1:]:  # Skip the first column (x values)
    #             # Calculate sum of squared differences between y_train and y_ideal
    #             squared_diff = ((self.train_data[train_col] - self.ideal_data[ideal_col]) ** 2).sum()
                
    #             # Find the minimum squared difference
    #             if squared_diff < min_squared_diff:
    #                 min_squared_diff = squared_diff
    #                 best_fit = ideal_col
            
    #         best_fit_functions[train_col] = best_fit
        
    #     return best_fit_functions
    
    def find_best_fit_functions(self):
        best_fit = []
        best_fit.append(self.train_data['x'])
        for col_train in self.train_data.columns[1:]:  # Iterate over each y column in the training data
            min_diff = np.inf
            best_func = None
            y_train = self.train_data[col_train]
            for col_ideal in self.ideal_data.columns[1:]:  # Iterate over each ideal y column
                y_ideal = self.ideal_data[col_ideal]
                squared_diff = ((y_train - y_ideal) ** 2).sum()  # Calculate sum of squared differences
                if squared_diff < min_diff:
                    min_diff = squared_diff
                    best_func = y_ideal
            best_fit.append(best_func)
        return pd.concat(best_fit, axis=1)  # Concatenate the best fit functions as a DataFrame
    
    # Function to map test data to the best fit ideal functions
    def map_test_data(file_path, best_fit, max_deviations):
        test_data = []
        mapped_data = []
        with open(file_path, mode="r") as file: # Iterate over each row in the test data
            reader = csv.reader(file)
            header = next(reader)  # Skip the header row if necessary.
            for row in reader:
                x_test, y_test = float(row[0]), float(row[1])
                test_data.append((x_test, y_test))
                min_deviation = np.inf
                best_fit_func = None
                best_deviation = None
                best_deviation_no_of_ideal_func = None
                for i, col_ideal in enumerate(best_fit.columns[1:]):
                    y_ideal_value = best_fit.loc[best_fit['x'] == x_test, col_ideal].values[0]
                    deviation = abs(y_test - y_ideal_value)
                    if deviation < min_deviation and deviation <= max_deviations[i]:
                        min_deviation = deviation
                        best_fit_func = i + 1  # Indicate which of the four ideal functions it corresponds to
                        best_deviation = deviation
                        best_deviation_no_of_ideal_func = col_ideal.removeprefix('y')
                if best_fit_func is not None:
                    mapped_data.append((
                        x_test,
                        y_test,
                        best_deviation,
                        best_deviation_no_of_ideal_func,
                        y_ideal_value
                    ))
        test_dataframe = pd.DataFrame(
            test_data,
            columns=['x','y']
        )
        mapped_dataframe = pd.DataFrame(
            mapped_data,
            columns=[
                'X (test func)',
                'Y (test func)',
                'Delta Y (test func)',
                'No.  of ideal func',
                'ideal_func_val'
            ]
        )
        return test_dataframe, mapped_dataframe 