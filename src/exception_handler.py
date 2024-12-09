class CustomException(Exception):
    """Base class for custom exceptions"""
    pass


class FileNotFoundError(CustomException):
    """Exception raised for missing files"""

    def __init__(self, message="File not found"):
        self.message = message
        super().__init__(self.message)


class DataProcessingError(CustomException):
    """Exception raised for errors during data processing"""

    def __init__(self, message="Error in data processing"):
        self.message = message
        super().__init__(self.message)


class DatabaseError(CustomException):
    """Exception raised for database-related errors"""

    def __init__(self, message="Database operation failed"):
        self.message = message
        super().__init__(self.message)


class DataVisualizationError(CustomException):
    """Exception raised for errors during data visualization"""

    def __init__(self, message="Error in data visualization"):
        self.message = message
        super().__init__(self.message)


def handle_exception(func):
    """Decorator to handle exceptions"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"An error occurred: {e}")
            raise
    return wrapper