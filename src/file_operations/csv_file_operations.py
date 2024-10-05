import pandas as pd
from file_operations.file_operations import FileOperations
from exception_handler import DataProcessingError

class CsvFileOperations(FileOperations):
    """Class for CSV file operations"""

    def read_csv(self, file_path):
        """Reads CSV file and returns a DataFrame"""
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise DataProcessingError(f"Error processing CSV file {file_path}: {str(e)}")