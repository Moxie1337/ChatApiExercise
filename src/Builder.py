import time
import logging
from pathlib import Path
from typing import List
from collections import OrderedDict

from src.QuestionFetcher import Fetcher
from src.Generator import Generator
from src.ChatFactory import ChatFactory
from src.IoProcess import CsvIOProcess
from src.LoggingConfig import setup_logger

chat_log = setup_logger()

class Builder:
    def __init__(self, *args, **kwargs):
        self.args_ = args[0]
        self.kwargs_ = kwargs
        
        self.message_path = self.args_.message_path
        self.repeat_nums = self.args_.repeat_nums
        self.range_ = tuple(self.args_.range)

        self.message_dict = OrderedDict()

    def get_more_detail_from_chat(self, messages : List):
        longest_message = max(messages, key=len)
        return longest_message

    def run(self) -> bool:
        
        chat_log.info(f'process message from [{self.range_[0]}, {self.range_[1]}).')

        message_fetcher = Fetcher(self.message_path, range_=self.range_).run()
        message_generator = Generator(message_fetcher).run()

        for idx, message in enumerate(message_generator):
            message_container = []
            chat_handle = ChatFactory("config/openai.json", message)

            # every query repeat `repeat_nums` times to get more detaile ans from chat
            for _ in range(self.repeat_nums):
                try:
                    chat_handle.create_chat()
                except Exception as e:
                    chat_log.error(f'{e},\nmessage from [{self.range_[0]}, {self.range_[0] + idx}) has beed processed \
                        \nplease restart this programme from --range [{self.range_[0] + idx},{self.range_[1]}).')
                    CsvIOProcess(self.args_, io_ops="output", message_dict=self.message_dict).run()                
                    return False
                
                time.sleep(1)
                message_container.append(chat_handle.get_chat_info())
  
            self.message_dict.update({str(idx + self.range_[0]) : self.get_more_detail_from_chat(message_container)})

            chat_log.info(f'No {idx + self.range_[0]} message has been processed!')

        CsvIOProcess(self.args_, io_ops="output", message_dict=self.message_dict).run()
        chat_log.info(f'all message has been processed! from idx [{self.range_[0]},{self.range_[1]})')

        return True
