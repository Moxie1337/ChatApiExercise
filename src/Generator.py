from typing import Iterator, Dict
# from QuestionFetcher import Fetcher

class ChatMessage:
    def __init__(self, role, content):
        self.role = role
        self.content = content
        self.messages = {"role": None, "content": None}
        self.set_message()

    def __call__(self) -> Dict:
        return self.messages

    def set_message(self):
        if self.get_message_length > 4095:
            self.content = self.content[:2000]
        self.messages.update({"role": self.role, "content": self.content})

    @property
    def get_message_length(self):
        return len(self.content)

class Generator:
    def __init__(self, content, role = "user", *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        
        self.role = role
        self.content_ = content
        self.content_length_ = 0
        self.prompt = None
        self.message_ = [None, None]
    
        if isinstance(self.content_, Iterator):
            self.prompt = next(self.content_)
            self.prompt_message = ChatMessage("system", self.prompt)()
            self.message_[0] = self.prompt_message

    def run(self) -> Iterator['Generator']:
        for content_message_ in self.content_:
            self.message_[1] = ChatMessage(self.role, content_message_)()
            yield self.message_

if __name__ == "__main__":
    fetcher_iter_ = Fetcher("dataset/question_set.xlsx")
    fetch_i = fetcher_iter_.run()
    gene = Generator(fetch_i).run()
    mess_ = next(gene)
    ChatMessage(mess_)
    
