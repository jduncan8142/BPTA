from abc import ABC, abstractmethod
from typing import List, Optional
from Core.Scenario import Scenario
from Core.Step import Step


class BusinessProcess(ABC):
    def __init__(self, name: str, owner: Optional[str] = "") -> None:
        super().__init__()
        self.__name: str = name
        self.__owner: str = owner
        self.__scenarios: list[Scenario] = []
        self.__tasks: list[Task] = []
    
    @property
    @abstractmethod
    def name(self) -> str:
        return self.__name
    
    @name.setter
    @abstractmethod
    def name(self, value: str) -> None:
        if type(value) is str:
            self.__name = value.upper()
        else:
            raise TypeError(f"type {type(value)} for 'value' not of type {str.__class__}")
    
    @property
    @abstractmethod
    def owner(self) -> str:
        return self.__owner
    
    @owner.setter
    @abstractmethod
    def owner(self, value: str) -> None:
        if type(value) is str:
            self.__owner = value.upper()
        else:
            raise TypeError(f"type {type(value)} for 'value' not of type {str.__class__}")
    
    @property
    @abstractmethod
    def scenarios(self) -> list:
        return ''.join(self.__scenarios)
    
    @scenarios.setter
    @abstractmethod
    def scenarios(self, value: List[Scenario] | Scenario) -> None:
        if isinstance(value, List(Scenario)):
            self.__scenarios = self.__scenarios + value
        elif isinstance(value, Scenario):
            self.__scenarios.append(value)
        else:
            raise TypeError(f"type {type(value)} for 'value' not of type {List.__class__} of {Scenario.__class__}s or {Scenario.__class__}")
    
    @scenarios.deleter
    @abstractmethod
    def remove_scenario(self, value: Scenario) -> None:
        for _index, _scenario in enumerate(self.__scenarios):
            if value == _scenario:
                _ = self.__scenarios.pop(_index)
    
    @property
    @abstractmethod
    def tasks(self) -> List(Task):
        return self.__tasks
    
    @tasks.setter
    @abstractmethod
    def tasks(self, value: List(Task) | Task) -> None:
        if isinstance(value, List(Task)):
            self.__tasks = self.__tasks + value
        elif isinstance(value, Task):
            self.__tasks.append(value)
        else:
            raise TypeError(f"type {type(value)} for 'value' not of type {List.__class__} of {Task.__class__}s or {Task.__class__}")
    
    @tasks.deleter
    @abstractmethod
    def remove_tasks(self, value: Task) -> None:
        for _index, _task in enumerate(self.__tasks):
            if value == _task:
                _ = self.__tasks.pop(_index)
