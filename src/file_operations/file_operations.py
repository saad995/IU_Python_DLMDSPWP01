import os
from exception_handler import FileNotFoundError

class FileOperations:
    """Base class for file operations"""

    def read_file(self, file_path):
        """Reads the file from the given path"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File {file_path} does not exist.")
        try:
            with open(file_path, 'r') as file:
                return file.read()
        except Exception as e:
            raise FileNotFoundError(f"Error reading file {file_path}: {str(e)}")