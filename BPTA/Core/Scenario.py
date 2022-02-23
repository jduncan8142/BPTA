from abc import ABC, abstractmethod
from Core.Base import Dict2Obj


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
