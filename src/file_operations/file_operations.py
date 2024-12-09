from abc import ABC, abstractmethod


class file_operations(ABC):
    """
    Abstract base class for file operations.
    This class defines the interface that all derived file operation classes must implement.
    """

    @abstractmethod
    def read_file(self, file_path):
        """
        Reads the file from the given path.
        :param file_path: File path as string.
        """
        pass
