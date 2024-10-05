import numpy as np
import pandas as pd
from data_processor.BestFitFinder import BestFitFinder
from file_operations.csv_file_operations import CsvFileOperations
from db_operations.sqlLite_db_operations import SQLiteDBOperations
from data_processor.train_data_processor import TrainDataProcessor
from data_processor.test_data_processor import TestDataProcessor
from data_visualizer.bokeh_data_visualizer import BokehDataVisualizer
import os

def main():
    try:
        # Remove database file if exists
        if os.path.exists("./data.db"):
            os.remove("./data.db")

        # File operations
        csv_ops = CsvFileOperations()
        train_data = csv_ops.read_csv('./dataset/train.csv')
        ideal_data = csv_ops.read_csv('./dataset/ideal.csv')
        test_data = csv_ops.read_csv('./dataset/test.csv')

        # Database operations
        db_ops = SQLiteDBOperations('sqlite:///data.db')
        db_ops.create_table('train_data', train_data.columns.values.tolist())
        train_data.to_sql('train_data', db_ops.engine, if_exists='replace', index = False)
        db_ops.create_table('ideal_data', ideal_data.columns.values.tolist())
        ideal_data.to_sql('ideal_data', db_ops.engine, if_exists='replace', index = False)
        test_data_columns = ['x', 'y', 'delta Y', 'no. of ideal func']
        db_ops.create_table('test_data_mapping', test_data_columns)

        # Data processing
        
        # Initialize the BestFitFinder with training and ideal data
        finder = BestFitFinder(train_data, ideal_data)

        # Find the best fit functions for each of the four training functions
        best_fit_functions = finder.find_best_fit_functions()

        # Print the results
        # for train_func, ideal_func in best_fit_functions.items():
        #     print(f"Best fit for {train_func} is {ideal_func}")

        # Calculate the maximum deviation allowed for mapping
        max_deviations = []
        for col_train, col_ideal in zip(train_data.columns[1:], best_fit_functions.columns):
            y_train = train_data[col_train]
            y_ideal = best_fit_functions[col_ideal]
            max_deviation = abs(y_train - y_ideal).max()
            max_deviations.append(max_deviation * np.sqrt(2))

        # Map the test data to the best fit ideal functions
        mapped_test_data = BestFitFinder.map_test_data(test_data, best_fit_functions, max_deviations)

        # The resulting DataFrame `mapped_test_data` contains the mapped test data with the deviation
        # print(mapped_test_data)

        # train_processor = TrainDataProcessor()
        # best_fit = train_processor.process_training_data(train_data, ideal_data)
        # test_processor = TestDataProcessor()
        # mapped_data = test_processor.map_test_data(test_data, ideal_data, train_data, best_fit)

        # Store test data with mapping and deviation


        # Data visualization
        visualizer = BokehDataVisualizer()
        visualizer.visualize_data(train_data['x'].values, train_data.drop(columns=['x']).values, best_fit_functions, test_data['x'].values, test_data['y'].values, np.array(mapped_test_data).T)

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()