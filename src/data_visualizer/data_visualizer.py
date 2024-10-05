from exception_handler import DataProcessingError


class DataVisualizer:
    """Base class for data visualization"""

    def visualize_data(self, data):
        """Visualizes the given data"""
        try:
            # This is a placeholder method, overridden by derived classes
            raise NotImplementedError("This method should be overridden by derived classes")
        except Exception as e:
            raise DataProcessingError(f"Error visualizing data: {str(e)}")