import os
import inspect
from typing import Any, Optional
import time
import win32con
import win32gui
from mss import mss
import datetime


def caller_name(skip=2):
    """Get a name of a caller in the format module.class.method

       `skip` specifies how many levels of stack to skip while getting caller
       name. skip=1 means "who calls me", skip=2 "who calls my caller" etc.

       An empty string is returned if skipped levels exceed stack height
    """
    stack = inspect.stack()
    start = 0 + skip
    if len(stack) < start + 1:
      return ''
    parentframe = stack[start][0]    

    name = []
    module = inspect.getmodule(parentframe)
    # `modname` can be None when frame is executed directly in console
    # TODO(techtonik): consider using __main__
    if module:
        name.append(module.__name__)
    # detect classname
    if 'self' in parentframe.f_locals:
        # I don't know any way to detect call from the object method
        # XXX: there seems to be no way to detect static method call - it will
        #      be just a function call
        name.append(parentframe.f_locals['self'].__class__.__name__)
    codename = parentframe.f_code.co_name
    if codename != '<module>':  # top level usually
        name.append( codename ) # function or a method

    ## Avoid circular refs and frame leaks
    #  https://docs.python.org/2.7/library/inspect.html#the-interpreter-stack
    del parentframe, stack

    return ".".join(name)


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


class Timer:
    """
    A basic timer to user when waiting some amount of time for a action or step to complete. 
    """
    def __init__(self) -> None:
        """
        Generates and starts a new timer
        """
        self.start_time = time.time()

    def elapsed(self) -> float:
        """
        Get the elapsed time since the timer was started/created in seconds

        Returns:
            float -- Seconds since timer was created and started
        """
        return time.time() - self.start_time


class WindowHandler:
    def __init__(self, window_description: Optional[str] = None) -> None:
        self.window_handle_list = []
        self.window_handle: str = None
        self.window_description: str = window_description if window_description is not None else ""
        if len(self.window_handle_list) == 0:
            self.gather_window_list()
    
    def winEnumHandler(self, hwnd: str, ctx: Any) -> None:
        if win32gui.IsWindowVisible(hwnd):
            self.window_handle_list.append((hwnd, win32gui.GetWindowText(hwnd)))
    
    def window_list_display(self, window_list: Optional[list] = None) -> None:
        _win_list = window_list if window_list is not None else self.window_handle_list
        import PySimpleGUI as sg
        layout = [[sg.Listbox(values=_win_list, size=(30, 6), enable_events=True, bind_return_key=True)]]
        window = sg.Window('Select Window', layout)
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Cancel':
                break
            else:
                window.close()
                if len(values) == 1:
                    v = values[0]
                    if len(v) == 1:
                        return v[0]
                    else:
                        return v
                else:
                    return values
    
    def gather_window_list(self) -> None:
        win32gui.EnumWindows(self.winEnumHandler, None)
    
    def close_window(self) -> None:
        self.window_handle = None
        for win in self.window_handle_list:
            if self.window_description == win[1]:
                self.window_handle = win[0]
            elif self.window_description in win[1]:
                self.window_handle = win[0] 
        if self.window_handle is not None:
            win32gui.PostMessage(self.window_handle, win32con.WM_CLOSE, 0, 0)


class Screenshot:
    """
    Screenshot functionality using the python mss module for documenting test results
    """
    def __init__(self) -> None:
        self.sct = mss()
        self.__directory: str = None
        self.__monitor: dict[str, int] = None
    
    @property
    def monitor(self) -> dict[str, int]:
        return self.__monitor
    
    @monitor.setter
    def monitor(self, value: int) -> None:
        self.__monitor = int(value)
    
    @property
    def screenshot_directory(self) -> str:
        return self.__directory
    
    @screenshot_directory.setter
    def screenshot_directory(self, value: str) -> None:
        __dir: str = os.path.join(os.getcwd(), value) 
        if not os.path.exists(__dir):
            try:
                os.mkdir(__dir)
            except Exception as err:
                raise FileNotFoundError(f"Directory {__dir} does not exist and was unable to be created automatically. Make sure you have the required access.")
        self.__directory = __dir
    
    def shot(self, monitor: Optional[int] = None, output: Optional[str] = None, name: Optional[str] = None, delay: Optional[float]= 2.0) -> list:
        if monitor:
            self.monitor(value=monitor)
        if output:
            self.screenshot_directory(value=output)
        else:
            if not self.__directory:
                self.screenshot_directory = "output"
        time.sleep(delay)
        __name = f"{name}.jpg" if name is not None else f"screenshot_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.jpg"
        return [x for x in self.sct.save(mon=self.__monitor, output=os.path.join(self.__directory, __name))]


# class BusinessProcess(ABC):
#     def __init__(self, name: str, owner: Optional[str] = "") -> None:
#         super().__init__()
#         self.__name: str = name
#         self.__owner: str = owner
#         self.__scenarios: list[Scenario] = []
#         self.__tasks: list[Task] = []
    
#     @property
#     @abstractmethod
#     def name(self) -> str:
#         return self.__name
    
#     @name.setter
#     @abstractmethod
#     def name(self, value: str) -> None:
#         if type(value) is str:
#             self.__name = value.upper()
#         else:
#             raise TypeError(f"type {type(value)} for 'value' not of type {str.__class__}")
    
#     @property
#     @abstractmethod
#     def owner(self) -> str:
#         return self.__owner
    
#     @owner.setter
#     @abstractmethod
#     def owner(self, value: str) -> None:
#         if type(value) is str:
#             self.__owner = value.upper()
#         else:
#             raise TypeError(f"type {type(value)} for 'value' not of type {str.__class__}")
    
#     @property
#     @abstractmethod
#     def scenarios(self) -> list:
#         return ''.join(self.__scenarios)
    
#     @scenarios.setter
#     @abstractmethod
#     def scenarios(self, value: List[Scenario] | Scenario) -> None:
#         if isinstance(value, List(Scenario)):
#             self.__scenarios = self.__scenarios + value
#         elif isinstance(value, Scenario):
#             self.__scenarios.append(value)
#         else:
#             raise TypeError(f"type {type(value)} for 'value' not of type {List.__class__} of {Scenario.__class__}s or {Scenario.__class__}")
    
#     @scenarios.deleter
#     @abstractmethod
#     def remove_scenario(self, value: Scenario) -> None:
#         for _index, _scenario in enumerate(self.__scenarios):
#             if value == _scenario:
#                 _ = self.__scenarios.pop(_index)
    
#     @property
#     @abstractmethod
#     def tasks(self) -> List(Task):
#         return self.__tasks
    
#     @tasks.setter
#     @abstractmethod
#     def tasks(self, value: List(Task) | Task) -> None:
#         if isinstance(value, List(Task)):
#             self.__tasks = self.__tasks + value
#         elif isinstance(value, Task):
#             self.__tasks.append(value)
#         else:
#             raise TypeError(f"type {type(value)} for 'value' not of type {List.__class__} of {Task.__class__}s or {Task.__class__}")
    
#     @tasks.deleter
#     @abstractmethod
#     def remove_tasks(self, value: Task) -> None:
#         for _index, _task in enumerate(self.__tasks):
#             if value == _task:
#                 _ = self.__tasks.pop(_index)


# class Scenario(ABC):
#     def __init__(self) -> None:
#         super().__init__()
#         self.__data__: dict
#         self.data: Dict2Obj
    
#     @property
#     @abstractmethod
#     def data(self) -> Dict2Obj:
#         return self.data
    
#     @data.setter
#     @abstractmethod
#     def data(self, value: dict) -> None:
#         if isinstance(value, dict):
#             self.__data__ = value
#             self.data = Dict2Obj(value)
#         elif isinstance(value, Dict2Obj):
#             self.data = value
#             self.__dict = value.__dict__()
#         else:
#             raise TypeError(f"type {type(value)} for 'value' not of type {Dict2Obj.__class__} or {dict.__class__}")


# class Status(ABC):
#     def __init__(self, action: object) -> None:
#         super().__init__()
#         self.__pass: bool = None
#         self.__fail: bool = None
#         self.__parent: Action
    
#     @abstractmethod
#     def current(self) -> str | None:
#         if self.__pass is True and self.__fail is False:
#             return "PASS"
#         elif self.__pass is False and self.__fail is True:
#             return "FAIL"
#         elif self.__pass is None and self.__fail is None:
#             return "None"
#         else:
#             raise ValueError(f"The pass/fail value for {self.__parent.__repr__} set incorrectly or not set")
    
#     @property
#     @abstractmethod
#     def action(self) -> str:
#         return self.__parent
    
#     @action.setter
#     @abstractmethod
#     def action(self, action: object) -> None:
#         if isinstance(action, Action):
#             self.__parent = action
#         else:
#             raise TypeError(f"type {type(action)} for 'action' not of type {Action.__class__}")
    
#     @abstractmethod
#     def passed(self) -> None:
#         self.__pass = True
#         self.__fail = False
    
#     @abstractmethod
#     def failed(self) -> None:
#         self.__pass = False
#         self.__fail = True
    
#     @property
#     @abstractmethod
#     def __str__(self) -> str:
#         try:
#             return self.current()
#         except ValueError:
#             return "ValueError"
    
#     @property
#     @abstractmethod
#     def __class__(self) -> str:
#         return f"<class 'Status'>"


# class Result(ABC):
#     def __init__(self, result: Any, error: Optional[str] = None) -> None:
#         super().__init__()
#         self.__result: Any = result
#         self.__error: str = error
#         self.__parent: Action

#     @property
#     @abstractmethod
#     def action(self) -> str:
#         return self.__parent
    
#     @action.setter
#     @abstractmethod
#     def action(self, action: object) -> None:
#         if isinstance(action, Action):
#             self.__parent = action
#         else:
#             raise TypeError(f"type {type(action)} for 'action' not of type {Action.__class__}")
    
#     @abstractmethod
#     def __repr__(self) -> str:
#         return f"<class 'Result': ('result': {self.__result}, 'error': {self.__error})>"
    
#     @property
#     @abstractmethod
#     def __class__(self) -> str:
#         return f"<class 'Result'>"
    
#     @property
#     @abstractmethod
#     def __dict__(self) -> dict:
#         return {'result': self.__result, 'error': self.__error, 'action': {self.__parent}}
    
#     @property
#     @abstractmethod
#     def __tuple__(self) -> tuple:
#         return tuple([self.__result, self.__error, self.__parent])


# class Action(ABC):
#     def __init__(self, function: str, *args, **kwargs) -> None:
#         super().__init__()
#         self.function: str = function
#         self.name = self.function.__name__
#         self.result: Result
#         self.status: Status
#         self.__parent: Step

#     @property
#     @abstractmethod
#     def step(self) -> str:
#         return self.__parent
    
#     @step.setter
#     @abstractmethod
#     def step(self, step: object) -> None:
#         if isinstance(step, Step):
#             self.__parent = step
#         else:
#             raise TypeError(f"type {type(step)} for 'step' not of type {Step.__class__}")

#     @property
#     @abstractmethod
#     def status(self) -> str:
#         return self.status
    
#     @status.setter
#     @abstractmethod
#     def status(self, status: object) -> None:
#         if isinstance(status, Status):
#             self.status = status
#         else:
#             raise TypeError(f"type {type(status)} for 'status' not of type {Status.__class__}")

#     @property
#     @abstractmethod
#     def result(self) -> str:
#         return self.result
    
#     @result.setter
#     @abstractmethod
#     def result(self, result: object) -> None:
#         if isinstance(result, Result):
#             self.result = result
#         else:
#             raise TypeError(f"type {type(result)} for 'result' not of type {Result.__class__}")
    
#     @abstractmethod
#     def __repr__(self) -> str:
#         return f"<class 'Action': ('name': {self.name}, 'function': {self.function})>"
    
#     @property
#     @abstractmethod
#     def __class__(self) -> str:
#         return f"<class 'Action'>"
    
#     @property
#     @abstractmethod
#     def __dict__(self) -> dict:
#         return {'name': self.name, 'function': self.function, 'result': self.result, 'status': self.status, 'step': self.__parent}
    
#     @property
#     @abstractmethod
#     def __tuple__(self) -> tuple:
#         return tuple([self.name, self.function, self.result, self.status, self.__parent])


# class Step(ABC):
#     def __init__(self) -> None:
#         super().__init__()
#         self.actions: List[Action]
#         self.status: PASS | FAIL
#         self.__parent: Task

#     @property
#     @abstractmethod
#     def task(self) -> str:
#         return self.__parent
    
#     @task.setter
#     @abstractmethod
#     def task(self, task: object) -> None:
#         if isinstance(task, Task):
#             self.__parent = task
#         else:
#             raise TypeError(f"type {type(task)} for 'task' not of type {Task.__class__}")

#     @property
#     @abstractmethod
#     def actions(self) -> str:
#         return self.actions
    
#     @actions.setter
#     @abstractmethod
#     def actions(self, actions: list[Action]) -> None:
#         if isinstance(actions, list[Action]):
#             self.actions = actions
#         else:
#             raise TypeError(f"type {type(actions)} for 'actions' not of type {list.__class__} of {Action.__class__}s")

#     @property
#     @abstractmethod
#     def status(self) -> str:
#         return self.status
    
#     @status.setter
#     @abstractmethod
#     def status(self, status: object) -> None:
#         if isinstance(status, Status):
#             self.status = status
#         else:
#             raise TypeError(f"type {type(status)} for 'status' not of type {Status.__class__}")

#     @abstractmethod
#     def __repr__(self) -> str:
#         return f"<class 'Step': ('actions': {self.actions}, 'status': {self.status})>"
    
#     @property
#     @abstractmethod
#     def __class__(self) -> str:
#         return f"<class 'Step'>"
    
#     @property
#     @abstractmethod
#     def __dict__(self) -> dict:
#         return {'actions': self.actions, 'status': self.status, 'task': self.__parent}
    
#     @property
#     @abstractmethod
#     def __tuple__(self) -> tuple:
#         return tuple([self.actions, self.status, self.__parent])


# class Task(ABC):
#     def __init__(self) -> None:
#         super().__init__()
#         self.scenarios: List[Scenario] = []
#         self.steps: List[Step] = []
#         self.status: Status
#         self.__parent: BusinessProcess

#     @property
#     @abstractmethod
#     def process(self) -> str:
#         return self.__parent
    
#     @process.setter
#     @abstractmethod
#     def process(self, process: object) -> None:
#         if isinstance(process, BusinessProcess):
#             self.__parent = process
#         else:
#             raise TypeError(f"type {type(process)} for 'process' not of type {BusinessProcess.__class__}")

#     @property
#     @abstractmethod
#     def scenarios(self) -> str:
#         return self.scenarios
    
#     @scenarios.setter
#     @abstractmethod
#     def scenarios(self, scenarios: list[Scenario] | Scenario) -> None:
#         if isinstance(scenarios, list[Scenario]):
#             self.scenarios = self.scenarios + scenarios
#         elif isinstance(scenarios, Scenario):
#             self.scenarios.append(scenarios)
#         else:
#             raise TypeError(f"type {type(scenarios)} for 'scenarios' not of type {list.__class__} of {Scenario.__class__}s or {Scenario.__class__}")

#     @property
#     @abstractmethod
#     def steps(self) -> str:
#         return self.steps
    
#     @steps.setter
#     @abstractmethod
#     def steps(self, steps: list[Step] | Step) -> None:
#         if isinstance(steps, list[Step]):
#             self.steps = self.steps + steps
#         elif isinstance(steps, Step):
#             self.steps.append(steps)
#         else:
#             raise TypeError(f"type {type(steps)} for 'steps' not of type {list.__class__} of {Step.__class__}s or {Step.__class__}")

#     @property
#     @abstractmethod
#     def status(self) -> str:
#         return self.status
    
#     @status.setter
#     @abstractmethod
#     def status(self, status: object) -> None:
#         if isinstance(status, Status):
#             self.status = status
#         else:
#             raise TypeError(f"type {type(status)} for 'status' not of type {Status.__class__}")

#     @abstractmethod
#     def __repr__(self) -> str:
#         return f"<class 'Task': ('scenarios': {self.scenarios}, 'steps': {self.steps})>"
    
#     @property
#     @abstractmethod
#     def __class__(self) -> str:
#         return f"<class 'Task'>"
    
#     @property
#     @abstractmethod
#     def __dict__(self) -> dict:
#         return {'scenarios': self.scenarios, 'steps': self.steps, 'status': self.status, 'process': self.__parent}
    
#     @property
#     @abstractmethod
#     def __tuple__(self) -> tuple:
#         return tuple([self.scenarios, self.steps, self.status, self.__parent])
