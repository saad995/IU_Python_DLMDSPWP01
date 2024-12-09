from abc import ABC, abstractmethod


class data_visualizer(ABC):
    """
    Abstract base class for data visualization.
    This class defines the interface that all derived data visualization classes must implement.
    """

    @abstractmethod
    def visualize_data(self, x_train, y_train, ideal_functions, x_test, y_test, mapped_data, current_dateTime):
        """
        Visualizes the given data, save the visualization as html file and show on browser as well.
        :param x_train: Column 'x' of the training dataset.
        :param y_train: Column 'y' of the training dataset.
        :param ideal_functions: Dataframe containing the best fit functions derived from the training and ideal datasets.
        :param x_test: Column 'x' of the test dataset.
        :param y_test: Column 'y' of the test dataset.
        :param mapped_data: Dataframe consisting of value of mapped function against the test dataset along with the deviation.
        :param current_dateTime: Current datetime to append in filename.
        """
        pass
