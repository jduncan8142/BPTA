from abc import ABC, abstractmethod
import importlib
from typing import Optional
from Core.Logger import Logger
from Core.Results import Results
from Core.Status import Status
from Core.Base import caller_name


class Action(ABC):
    def __init__(self, module: str, function: str, package: Optional[str | list[str]] = None, logger: Optional[Logger] = None, *args, **kwargs) -> None:
        super().__init__()
        self.__error: Optional[str] = None
        self.log = logger.log if logger is not None else Logger()
        self.module = None
        self.function = None
        self.name = None
        self.__package__ = package if package is not None else None
        self.__module__ = module
        try:
            if (spec := importlib.util.find_spec(self.__module__, package=self.__package__)) is not None:
                self.module = importlib.import_module(spec, package=self.__package__)
        except ModuleNotFoundError as err:
            self.__error = err
            self.log.critical(err)
        self.__function__: str = function
        try:
            self.function = getattr(self.module, self.__function__)
        except AttributeError as err:
            self.__error = err
            self.log.critical(err)
        try:
            self.name = caller_name()
        except Exception as err:
            self.name: str = f"{self.__package__}.{self.module.__name__}.{self.function.__name__}" if self.__package__ is not None else f"{self.module.__name__}.{self.function.__name__}"
            self.__error = err
            self.log.critical(err)            
        self.__results = Results()
        self.__status = Status()
        try:
            self.__results.results = self.function(*args, **kwargs)
        except Exception as err:
            self.__results.error = err
        self.status: Status
        self.__parent: caller_name()

    @property
    @abstractmethod
    def status(self) -> str:
        return self.__status

    @property
    @abstractmethod
    def result(self) -> str:
        return self.__result
    
    @abstractmethod
    def __repr__(self) -> str:
        return f"<class 'Action': ('name': {self.name}, 'function': {self.function})>"
    
    @property
    @abstractmethod
    def __class__(self) -> str:
        return f"<class 'Action'>"
    
    @property
    @abstractmethod
    def __dict__(self) -> dict:
        return {'name': self.name, 'function': self.function, 'result': self.result, 'status': self.status, 'step': self.__parent}
    
    @property
    @abstractmethod
    def __tuple__(self) -> tuple:
        return tuple([self.name, self.function, self.result, self.status, self.__parent])
