from abc import ABC, abstractmethod
from typing import Any, Optional
from Core.Base import caller_name


class Results(ABC):
    def __init__(self) -> None:
        super().__init__()
        self.__result: Optional[Any] = None
        self.__error: Optional[str] = None
        self.__parent = caller_name()
    
    @abstractmethod
    def __repr__(self) -> str:
        return f"<class 'Results': ('result': {self.__result}, 'error': {self.__error})>"
    
    @property
    @abstractmethod
    def __class__(self) -> str:
        return f"<class 'Result'>"
    
    @property
    @abstractmethod
    def __dict__(self) -> dict:
        return {'result': self.__result, 'error': self.__error, 'parent': {self.__parent}}
    
    @property
    @abstractmethod
    def __tuple__(self) -> tuple:
        return tuple([self.__result, self.__error, self.__parent])
