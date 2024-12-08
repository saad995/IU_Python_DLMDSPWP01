import numpy as np
from data_processor.BestFitFinder import BestFitFinder
from file_operations.csv_file_operations import CsvFileOperations
from db_operations.sqlLite_db_operations import SQLiteDBOperations
from data_visualizer.bokeh_data_visualizer import BokehDataVisualizer
from datetime import datetime

def main():
    try:        
        current_dateTime = datetime.now().strftime("%d%m%Y_%H%M%S") # Formatted date for filenames

        # File operations
        csv_ops = CsvFileOperations()
        train_data = csv_ops.read_csv('./dataset/train.csv')
        ideal_data = csv_ops.read_csv('./dataset/ideal.csv')

        # Database operations
        db_ops = SQLiteDBOperations(f"sqlite:///database/data_{current_dateTime}.db")
        db_ops.create_table('train_data', train_data.columns.values.tolist())
        train_data.to_sql('train_data', db_ops.engine, if_exists='replace', index = False)
        db_ops.create_table('ideal_data', ideal_data.columns.values.tolist())
        ideal_data.to_sql('ideal_data', db_ops.engine, if_exists='replace', index = False)
        test_data_columns = ['X (test func)', 'Y (test func)', 'Delta Y (test func)', 'No.  of ideal func']
        db_ops.create_table('test_data_mapping', test_data_columns)

        # Data processing
        # Initialize the BestFitFinder with training and ideal data
        finder = BestFitFinder(train_data, ideal_data)

        # Find the best fit functions for each of the four training functions
        best_fit_functions = finder.find_best_fit_functions()

        # Calculate the maximum deviation allowed for mapping
        max_deviations = []
        for col_train, col_ideal in zip(train_data.columns[1:], best_fit_functions.columns[1:]):
            y_train = train_data[col_train]
            y_ideal = best_fit_functions[col_ideal]
            max_deviation = abs(y_train - y_ideal).max()
            max_deviations.append(max_deviation * np.sqrt(2))

        # Map the test data to the best fit ideal functions
        test_data, mapped_test_data = BestFitFinder.map_test_data(
            './dataset/test.csv',
            best_fit_functions,
            max_deviations
        )
        mapped_test_data_ordered = mapped_test_data.sort_values('X (test func)', ascending=True)

        # Store test data with mapping and deviation
        # Convert DataFrame to a list of dictionaries
        mapped_test_data_ordered_as_dicts = mapped_test_data_ordered.to_dict(orient='records')
        db_ops.insert_data('test_data_mapping', mapped_test_data_ordered_as_dicts)

        # Data visualization
        visualizer = BokehDataVisualizer()
        test_data_ordered = test_data.sort_values('x')
        visualizer.visualize_data(
            train_data['x'].values,
            train_data.drop(columns=['x']).values,
            best_fit_functions,
            test_data_ordered['x'].values,
            test_data_ordered['y'].values,
            mapped_test_data_ordered,
            current_dateTime
        )

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()