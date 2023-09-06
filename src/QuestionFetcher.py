from typing import Iterator
from itertools import chain
import pandas as pd

# csv_ = pd.DataFrame(pd.read_excel("dataset/question_set.xlsx", 
#                                     engine="openpyxl"))

class Fetcher:
    def __init__(self, csv_path, range_ = (1141, 1325)):
        # csv_path "dataset/question_set.xlsx"
        self.csv_path = csv_path
        self.csv_data = None
        self.range_ = range_
        self.engine_ = "openpyxl"

        self.extra_info = ["假设你是一个安全分析人员，主要是对web请求和响应进行分析，只针对给出的信息进行分析，不用提供建议。如果给出的信息中，攻击任务没有被执行，则可以认为攻击失败，不需要再结合系统设置、系统环境等要素再确定。"]
        self.cvt_basic_statement = lambda x: '\n'.join(x.splitlines()[:-1]) + "\n" + ''.join(x.splitlines()[-1].split('？')[:-1]) + '？'
    
    # def __call__(self) -> Iterator['Fetcher']:
    #     pass

    def set_data(self, key, value):
        self.csv_data[key] = value

    def get_full_csv_data(self):
        return pd.DataFrame(pd.read_excel(self.csv_path, engine=self.engine_))
    
    def preprocess_csv_data(self):
        self.csv_data = self.get_full_csv_data()
        d_ = pd.DataFrame(self.csv_data.get("concatenated_text").apply(self.cvt_basic_statement))
        self.csv_data["formated_content"] = d_

    def get_csv_by_range(self,  keys , range):
        if len(range) == 1:
            return self.csv_data.get(keys).iloc[range[0] : range[0] + 1]
        elif len(range) == 2: 
            return self.csv_data.get(keys).iloc[range[0] : range[1]]
        else:
            raise IndexError
        
    def run(self) -> Iterator['Fetcher']:
        self.preprocess_csv_data()
        formated_data_ = self.get_csv_by_range("formated_content" , self.range_)
        yield from iter(chain(self.extra_info, formated_data_))


if __name__ == "__main__":
    fetcher_iter_ = Fetcher("dataset/question_set.xlsx")
    print(list(fetcher_iter_.run()))
    