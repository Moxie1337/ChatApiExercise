import json
from pathlib import Path
from abc import ABC, abstractmethod

from typing import Dict

class IOProcess(ABC):
    _register = {}

    def __init_subclass__(cls, file_type_="csv", **kwargs):
        super().__init_subclass__(**kwargs) 
        if cls._register.get(file_type_) is None:
            cls._register.update({file_type_: cls})

    @abstractmethod
    def run(self) -> bool:
        pass

class CsvIOProcess(IOProcess, file_type_="csv"):

    def __init__(self, *args, io_ops="output", message_dict, **kwargs):
        self.args_ = args[0]
        self.kwargs_ = kwargs

        self.io_ops_ = io_ops
        self.message_dict_ = message_dict
        self.save_path_ = self.args_.save_path
        self.clear_old_message_ = self.args_.clear_old_message

        self.save_file_handle = Path(self.save_path_)

    def merge_message_dict(self, new_message_dict_) -> Dict:
        _origin_message_dict = json.loads(self.save_file_handle.read_text())
        return {**_origin_message_dict, **new_message_dict_}

    def save_file(self):
        if self.save_file_handle.is_file():
            if not self.clear_old_message_:
                self.message_dict_ = self.merge_message_dict(self.message_dict_)

        self.save_file_handle.write_text(json.dumps(
                                    self.message_dict_, indent=4, ensure_ascii=False))

    def read_file(self):
        pass

    def run(self):
        if self.io_ops_ == "output":
            self.save_file()
        elif self.io_ops_ == "input":
            self.read_file()
        else:
            raise KeyError("Wrong io_ops, only support `input` and `output` mode.")

"""add some code to handle other_type's file"""
# class OtherProcess(IOProcess, file_type="other"):
#     def run(self):
#         pass
