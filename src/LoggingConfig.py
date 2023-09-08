from __future__ import absolute_import

import logging

def setup_logger(level=logging.INFO):
    l = logging.getLogger("ChatLog")
    formatter = logging.Formatter('"%(asctime)s [%(levelname)s] %(message)s"')
    fileHandler = logging.FileHandler("config/log.config", mode='w')
    fileHandler.setFormatter(formatter)
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)

    l.setLevel(level)
    l.addHandler(fileHandler)
    l.addHandler(streamHandler)    


if '__main__' == __name__:

    def main():
        setup_logger()
        log = logging.getLogger("ChatLog")

        log.info('Info for log 1!')
        log.error('Oh, no! Something went wrong!')

    main()