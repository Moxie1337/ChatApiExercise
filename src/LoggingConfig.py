from __future__ import absolute_import

import logging

def setup_logger(level=logging.INFO):
    l = logging.getLogger("ChatLog")
    formatter = logging.Formatter('"%(asctime)s [%(levelname)s] %(message)s"')
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)

    l.setLevel(level)
    l.addHandler(streamHandler)    

    return l

if '__main__' == __name__:

    def main():
        log = setup_logger()
        log.info('Info for log 1!')
        log.error('Oh, no! Something went wrong!')

    main()