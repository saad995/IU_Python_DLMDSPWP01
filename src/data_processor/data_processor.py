from exception_handler import DataProcessingError

class DataProcessor:
    """Base class for data processing operations"""

    def process_data(self, data):
        """Processes the data"""
        try:
            # Example of a processing step: Normalizing the data
            normalized_data = (data - data.mean()) / data.std()
            return normalized_data
        except Exception as e:
            raise DataProcessingError(f"Data processing error: {str(e)}")