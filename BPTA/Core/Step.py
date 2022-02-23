from abc import ABC, abstractmethod
from typing import Any, List, Optional
from Core.Task import Task


class Step(ABC):
    def __init__(self) -> None:
        super().__init__()
        self.actions: List[Action]
        self.status: PASS | FAIL
        self.__parent: Task

    @property
    @abstractmethod
    def task(self) -> str:
        return self.__parent
    
    @task.setter
    @abstractmethod
    def task(self, task: object) -> None:
        if isinstance(task, Task):
            self.__parent = task
        else:
            raise TypeError(f"type {type(task)} for 'task' not of type {Task.__class__}")

    @property
    @abstractmethod
    def actions(self) -> str:
        return self.actions
    
    @actions.setter
    @abstractmethod
    def actions(self, actions: list[Action]) -> None:
        if isinstance(actions, list[Action]):
            self.actions = actions
        else:
            raise TypeError(f"type {type(actions)} for 'actions' not of type {list.__class__} of {Action.__class__}s")

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
        return f"<class 'Step': ('actions': {self.actions}, 'status': {self.status})>"
    
    @property
    @abstractmethod
    def __class__(self) -> str:
        return f"<class 'Step'>"
    
    @property
    @abstractmethod
    def __dict__(self) -> dict:
        return {'actions': self.actions, 'status': self.status, 'task': self.__parent}
    
    @property
    @abstractmethod
    def __tuple__(self) -> tuple:
        return tuple([self.actions, self.status, self.__parent])
