from business_logic_layer.best_fit_finder import best_fit_finder
from exception_handler import handle_exception
from file_operations.csv_file_operations import csv_file_operations
from db_operations.sqlLite_db_operations import sqlLite_db_operations
from data_visualizer.bokeh_data_visualizer import bokeh_data_visualizer
from datetime import datetime


@handle_exception
def main():
    dt_format = '%d%m%Y_%H%M%S'
    current_dt = datetime.now().strftime(dt_format)  # Formatted date for filenames
    train_data_filepath = './dataset/train.csv'
    train_data_tablename = 'train_data'
    ideal_data_filepath = './dataset/ideal.csv'
    ideal_data_tablename = 'ideal_data'
    test_data_filepath = './dataset/test.csv'
    test_data_mapping_tablename = 'test_data_mapping'

    # File operations : Reading CSV files using our csv_file_operations class
    csv_ops = csv_file_operations()
    train_dataframe = csv_ops.read_file(train_data_filepath)
    ideal_dataframe = csv_ops.read_file(ideal_data_filepath)

    # Database operations : Creating SQL lite database and tables to store training data along with ideal data
    db_ops = sqlLite_db_operations(f"sqlite:///database/data_{current_dt}.db")
    db_ops.create_table(train_data_tablename,
                        train_dataframe.columns.values.tolist())
    train_dataframe.to_sql(train_data_tablename, db_ops.engine,
                           if_exists='replace', index=False)
    db_ops.create_table(ideal_data_tablename,
                        ideal_dataframe.columns.values.tolist())
    ideal_dataframe.to_sql(ideal_data_tablename, db_ops.engine,
                           if_exists='replace', index=False)
    test_data_columns = ['X (test func)', 'Y (test func)',
                         'Delta Y (test func)', 'No.  of ideal func']
    db_ops.create_table(test_data_mapping_tablename, test_data_columns)

    # Finding the best fit functions against training data and ideal data
    bestFitFinder = best_fit_finder(train_dataframe, ideal_dataframe)   # Initialize the BestFitFinder with training and ideal data
    bestFitFinder.find_best_fit_functions()     # Find the best fit functions for each of the four training functions
    bestFitFinder.calculate_max_deviations()    # Calculate the maximum deviation allowed for mapping
    bestFitFinder.map_test_data(test_data_filepath) # Map the test data to the best fit ideal functions

    # Store test data with mapping and deviation
    mapped_test_data_ordered = bestFitFinder.mapped_dataframe.sort_values('X (test func)', ascending=True)    # Ordering mapped test data in ascending w.r.t column X (test func)
    mapped_test_data_ordered_as_dicts = mapped_test_data_ordered.to_dict(orient='records')  # Convert DataFrame to a list of dictionaries
    db_ops.insert_data(test_data_mapping_tablename, mapped_test_data_ordered_as_dicts)

    # Data visualization
    visualizer = bokeh_data_visualizer()
    test_data_ordered = bestFitFinder.test_dataframe.sort_values('x')
    visualizer.visualize_data(
        train_dataframe['x'].values,
        train_dataframe.drop(columns=['x']).values,
        bestFitFinder.best_fit_functions,
        test_data_ordered['x'].values,
        test_data_ordered['y'].values,
        mapped_test_data_ordered,
        current_dt
    )


if __name__ == "__main__":
    main()
