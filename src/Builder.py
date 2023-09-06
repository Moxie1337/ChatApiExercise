
import argparse
import textwrap
import time
import json
from pathlib import Path
from typing import List
from collections import OrderedDict

from openai.error import RateLimitError

from src.QuestionFetcher import Fetcher
from src.Generator import Generator
from src.ChatFactory import ChatFactory

class Builder:
    def __init__(self, *args, **kwargs):
        self.args_ = args[0]
        self.kwargs_ = kwargs
        
        self.message_path = self.args_.message_path
        self.save_path = self.args_.save_path
        self.repeat_nums = self.args_.repeat_nums
        self.range_ = tuple(self.args_.range)
        self.message_dict = OrderedDict()

    def get_more_detail_from_chat(self, messages : List):
        longest_message = max(messages, key=len)
        return longest_message

    def run(self):

        message_fetcher = Fetcher(self.message_path, range_=self.range_).run()
        message_generator = Generator(message_fetcher).run()

        for idx, message in enumerate(message_generator):
            message_container = []
            chat_handle = ChatFactory("config/openai.json", message)

            # every query repeat `repeat_nums` times to get more detaile ans from chat
            for i in range(self.repeat_nums):
                try:
                    chat_handle.create_chat()
                except RateLimitError:
                    time.sleep(10)
                    chat_handle.create_chat()
                message_container.append(chat_handle.get_chat_info())
                time.sleep(1)
                
            self.message_dict.update({idx: self.get_more_detail_from_chat(message_container)})
            print(f'No {idx + self.range_[0]} message processed!')
        Path(self.save_path).write_text(json.dumps(self.message_dict, indent=4))

if __name__ == "__main__":
    Builder(args)
