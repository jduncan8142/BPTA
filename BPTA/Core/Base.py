from abc import ABC, abstractmethod
from os import access
from typing import Any, List, Optional


class Dict2Obj(dict):
    def __init__(self, dict_: dict) -> None:
        super(Dict2Obj, self).__init__(dict_)
        for key in self:
            item = self[key]
            if isinstance(item, list):
                for idx, it in enumerate(item):
                    if isinstance(it, dict):
                        item[idx] = Dict2Obj(it)
            elif isinstance(item, dict):
                self[key] = Dict2Obj(item)

    def __getattr__(self, key: Any) -> Any:
        return self[key]
    
    def __setattr__(self, key: str, value: Any) -> None:
        self.__setattr__(key, value)
    
    def __setitem__(self, key: str, value: Any) -> None:
        self.__setitem__(key, value)


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


class Scenario(ABC):
    def __init__(self) -> None:
        super().__init__()
        self.__data__: dict
        self.data: Dict2Obj
    
    @property
    @abstractmethod
    def data(self) -> Dict2Obj:
        return self.data
    
    @data.setter
    @abstractmethod
    def data(self, value: dict) -> None:
        if isinstance(value, dict):
            self.__data__ = value
            self.data = Dict2Obj(value)
        elif isinstance(value, Dict2Obj):
            self.data = value
            self.__dict = value.__dict__()
        else:
            raise TypeError(f"type {type(value)} for 'value' not of type {Dict2Obj.__class__} or {dict.__class__}")


class Status(ABC):
    def __init__(self, action: object) -> None:
        super().__init__()
        self.__pass: bool = None
        self.__fail: bool = None
        self.__parent: Action
    
    @abstractmethod
    def current(self) -> str | None:
        if self.__pass is True and self.__fail is False:
            return "PASS"
        elif self.__pass is False and self.__fail is True:
            return "FAIL"
        elif self.__pass is None and self.__fail is None:
            return "None"
        else:
            raise ValueError(f"The pass/fail value for {self.__parent.__repr__} set incorrectly or not set")
    
    @property
    @abstractmethod
    def action(self) -> str:
        return self.__parent
    
    @action.setter
    @abstractmethod
    def action(self, action: object) -> None:
        if isinstance(action, Action):
            self.__parent = action
        else:
            raise TypeError(f"type {type(action)} for 'action' not of type {Action.__class__}")
    
    @abstractmethod
    def passed(self) -> None:
        self.__pass = True
        self.__fail = False
    
    @abstractmethod
    def failed(self) -> None:
        self.__pass = False
        self.__fail = True
    
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


class Result(ABC):
    def __init__(self, result: Any, error: Optional[str] = None) -> None:
        super().__init__()
        self.__result: Any = result
        self.__error: str = error
        self.__parent: Action

    @property
    @abstractmethod
    def action(self) -> str:
        return self.__parent
    
    @action.setter
    @abstractmethod
    def action(self, action: object) -> None:
        if isinstance(action, Action):
            self.__parent = action
        else:
            raise TypeError(f"type {type(action)} for 'action' not of type {Action.__class__}")
    
    @abstractmethod
    def __repr__(self) -> str:
        return f"<class 'Result': ('result': {self.__result}, 'error': {self.__error})>"
    
    @property
    @abstractmethod
    def __class__(self) -> str:
        return f"<class 'Result'>"
    
    @property
    @abstractmethod
    def __dict__(self) -> dict:
        return {'result': self.__result, 'error': self.__error, 'action': {self.__parent}}
    
    @property
    @abstractmethod
    def __tuple__(self) -> tuple:
        return tuple([self.__result, self.__error, self.__parent])


class Action(ABC):
    def __init__(self, function: str, *args, **kwargs) -> None:
        super().__init__()
        self.function: str = function
        self.name = self.function.__name__
        self.result: Result
        self.status: Status
        self.__parent: Step

    @property
    @abstractmethod
    def step(self) -> str:
        return self.__parent
    
    @step.setter
    @abstractmethod
    def step(self, step: object) -> None:
        if isinstance(step, Step):
            self.__parent = step
        else:
            raise TypeError(f"type {type(step)} for 'step' not of type {Step.__class__}")

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

    @property
    @abstractmethod
    def result(self) -> str:
        return self.result
    
    @result.setter
    @abstractmethod
    def result(self, result: object) -> None:
        if isinstance(result, Result):
            self.result = result
        else:
            raise TypeError(f"type {type(result)} for 'result' not of type {Result.__class__}")
    
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
