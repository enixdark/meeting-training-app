from abc import abstractmethod, ABC


class ApplicationException(Exception, ABC):
    def __init__(self):
        self.__message = self._create_exception_message()
        self.__response_code = self._create_exception_response_code()
        super().__init__(self.__message)

    @abstractmethod
    def _create_exception_message(self) -> str:
        pass

    @abstractmethod
    def _create_exception_response_code(self) -> int:
        pass

    def get_response_code(self) -> int:
        return self.__response_code

    def get_message(self) -> str:
        return self.__message
