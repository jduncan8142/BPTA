from abc import ABC, abstractmethod
from typing import Optional
from Core.Base import caller_name


class Status(ABC):
    def __init__(self) -> None:
        super().__init__()
        self.__pass: bool = False
        self.__fail: bool = False
        self.__error: Optional[str] = None
        self.__parent = caller_name()
    
    @abstractmethod
    def current(self) -> str | None:
        if self.__pass and not self.__fail:
            return "PASS"
        elif not self.__pass and self.__fail:
            return "FAIL"
        elif not self.__pass and not self.__fail:
            return None
        else:
            self.__error = ValueError(f"The pass/fail value for {self.__parent.__repr__()} set incorrectly or not set")
            return "UNKNOWN"
    
    @abstractmethod
    def passed(self) -> None:
        self.__pass = True
        self.__fail = False
    
    @abstractmethod
    def failed(self) -> None:
        self.__pass = False
        self.__fail = True
    
    @abstractmethod
    def __repr__(self) -> str:
        return f"<class 'Status': ('value': {self.current()}, 'error': {self.__error})>"
    
    @property
    @abstractmethod
    def __str__(self) -> str:
        try:
            return self.current()
        except ValueError:
            return "ValueError"
    
    @property
    @abstractmethod
    def __class__(self) -> str:
        return f"<class 'Status'>"
    
    @property
    @abstractmethod
    def __dict__(self) -> dict:
        return {'value': self.current(), 'error': self.__error, 'parent': {self.__parent}}
    
    @property
    @abstractmethod
    def __tuple__(self) -> tuple:
        return tuple([self.current(), self.__error, self.__parent])
