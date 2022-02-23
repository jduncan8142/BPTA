from abc import ABC, abstractmethod
from typing import Any, List, Optional
from Core.Action import Action


class Task(ABC):
    def __init__(self) -> None:
        super().__init__()
        self.scenarios: List[Scenario] = []
        self.steps: List[Step] = []
        self.status: Status
        self.__parent: BusinessProcess

    @property
    @abstractmethod
    def process(self) -> str:
        return self.__parent
    
    @process.setter
    @abstractmethod
    def process(self, process: object) -> None:
        if isinstance(process, BusinessProcess):
            self.__parent = process
        else:
            raise TypeError(f"type {type(process)} for 'process' not of type {BusinessProcess.__class__}")

    @property
    @abstractmethod
    def scenarios(self) -> str:
        return self.scenarios
    
    @scenarios.setter
    @abstractmethod
    def scenarios(self, scenarios: list[Scenario] | Scenario) -> None:
        if isinstance(scenarios, list[Scenario]):
            self.scenarios = self.scenarios + scenarios
        elif isinstance(scenarios, Scenario):
            self.scenarios.append(scenarios)
        else:
            raise TypeError(f"type {type(scenarios)} for 'scenarios' not of type {list.__class__} of {Scenario.__class__}s or {Scenario.__class__}")

    @property
    @abstractmethod
    def steps(self) -> str:
        return self.steps
    
    @steps.setter
    @abstractmethod
    def steps(self, steps: list[Step] | Step) -> None:
        if isinstance(steps, list[Step]):
            self.steps = self.steps + steps
        elif isinstance(steps, Step):
            self.steps.append(steps)
        else:
            raise TypeError(f"type {type(steps)} for 'steps' not of type {list.__class__} of {Step.__class__}s or {Step.__class__}")

    @property
    @abstractmethod
    def status(self) -> str:
        return self.status
    
    @status.setter
    @abstractmethod
    def status(self, status: object) -> None:
        if isinstance(status, Status):
            self.status = status
        else:
            raise TypeError(f"type {type(status)} for 'status' not of type {Status.__class__}")

    @abstractmethod
    def __repr__(self) -> str:
        return f"<class 'Task': ('scenarios': {self.scenarios}, 'steps': {self.steps})>"
    
    @property
    @abstractmethod
    def __class__(self) -> str:
        return f"<class 'Task'>"
    
    @property
    @abstractmethod
    def __dict__(self) -> dict:
        return {'scenarios': self.scenarios, 'steps': self.steps, 'status': self.status, 'process': self.__parent}
    
    @property
    @abstractmethod
    def __tuple__(self) -> tuple:
        return tuple([self.scenarios, self.steps, self.status, self.__parent])
