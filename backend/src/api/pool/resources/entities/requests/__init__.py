from abc import ABC, abstractmethod


class Request(ABC):
    """
    Get all data
    """

    @abstractmethod
    def all(self):
        pass

    """
    Get data with specific keyword
    """

    @abstractmethod
    def get(self, keyword):
        pass

    """
    Get headers
    """

    @abstractmethod
    def header(self, name=''):
        pass

    """
    Get method
    """

    @abstractmethod
    def method(self):
        pass

    """
    Get decoded authentication
    """

    @abstractmethod
    def get_authentication(self):
        pass
