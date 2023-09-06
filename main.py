from pathlib import Path
from typing import List
from openai.error import InvalidRequestError
from collections import OrderedDict
import json
import time

from src.QuestionFetcher import Fetcher
from src.Generator import Generator
from src.ChatFactory import ChatFactory

def get_more_detail_from_chat(messages : List):
    longest_message = max(messages, key=len)
    return longest_message

if __name__ == "__main__":

    message_dict = OrderedDict()
    save_path = "ans.txt"

    message_fetcher = Fetcher("dataset/question_set.xlsx").run()
    message_generator = Generator(message_fetcher).run()

    for idx, message in enumerate(message_generator):
        message_container = []
        chat_handle = ChatFactory("config/openai.json", message)

        # every query repeat 3 times to get more detaile ans from chat
        for i in range(3):
            try:
                chat_handle.create_chat()
            except InvalidRequestError:
                time.sleep(10)
                chat_handle.create_chat()
            message_container.append(chat_handle.get_chat_info())

        message_dict.update({idx: get_more_detail_from_chat(message_container)})
        print(f'No{idx} message processed!')
    Path(save_path).write_text(json.dumps(message_dict, indent=4))

        

