import os
import argparse
import textwrap

from src.Builder import Builder

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
                            This project used for acadamic query, do not waste or sell api_key.                                      
                        '''))

    parser.add_argument('--range', metavar='N', type=int, nargs='+', default=[1, 3],
                    help = 'a range of message processed, please input 2 num represent `[start, end)`')

    parser.add_argument('--message_path',type=str, default="dataset/question_set.xlsx",
                    help = 'where the message files are stored')

    parser.add_argument("--save_path", type=str, default="ans.txt",
                        help = "the save path of queried message")
    
    parser.add_argument("--repeat_nums", type=int, default=2,
                        help = "The number of times GPT repeatedly asked the same question")
    

    args = parser.parse_args()

    Builder(args).run()

    os._exit(-1)

        

