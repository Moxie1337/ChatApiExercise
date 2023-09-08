import os
import argparse
import textwrap

from src.Builder import Builder

def str2bool(value):
    if isinstance(value, bool):
        return value
    if value.lower() in {'false', 'f', '0', 'no', 'n'}:
        return False
    elif value.lower() in {'true', 't', '1', 'yes', 'y'}:
        return True
    raise ValueError(f'{value} is not a valid boolean value')

class FormatHelp(argparse.RawTextHelpFormatter):
    pass

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
                    prog='ChatGPT query',
                    description='automated query ChatGPT using GPT api',
                    formatter_class=FormatHelp,
                    epilog=textwrap.dedent('''\
                            Here are some explanations about the parameters and code.                                            
                            python3 main.py --range 1 3 --message_path dataset/question_set.xlsx --save_path ans.txt --repeat_nums 2           
                            using ChatGPT api process message_path's file from idx[1:3), each message is repeatedly asked for 2 times, 
                                           while save processed message to save_path.
                            This project used for acadamic query, do not waste or sell api_key :).                                      
                        '''))

    parser.add_argument('--range', metavar='N', type=int, nargs='+', default=[1, 3],
                    help = 'A range of message processed, please input 2 num represent `[start, end)`.')

    parser.add_argument('--message_path',type=str, default="dataset/question_set.xlsx",
                    help = 'Where the message files are stored.')

    parser.add_argument("--save_path", type=str, default="ans.txt",
                        help = "The save path of queried message.")
    
    parser.add_argument("--repeat_nums", type=int, default=2,
                        help = "The number of times GPT repeatedly asked the same question.")
    
    parser.add_argument("--clear_old_message", type=str2bool, nargs='?', default=False, const=True,
                        help = "A boolean flag indicate whether to delete old message file.")
    

    args = parser.parse_args()

    res = Builder(args).run()

    os._exit(res)
