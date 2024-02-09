import logging
import logging.handlers
import os
from logging import Handler, Formatter
import datetime
import queue

import requests


class TelegramRequestsHandler(Handler):
    def emit(self, record):
        log_entry = self.format(record)
        payload = {
            'chat_id': os.getenv('TELEGRAM_CHAT_ID'),
            'text': log_entry,
            'parse_mode': 'HTML'
        }
        return requests.post("https://api.telegram.org/bot{token}/sendMessage".format(token=os.getenv('TELEGRAM_TOKEN')),data=payload).content


class LogstashFormatter(Formatter):
    def __init__(self):
        super(LogstashFormatter, self).__init__()

    def format(self, record):
        t = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

        if isinstance(record.msg, dict):
            message = "<i>{datetime}</i>".format(datetime=t)

            for key in record.msg:
                message = message + ("<pre>\n{title}: <strong>{value}</strong></pre>".format(title=key, value=record.msg[key]))

            return message
        else:
            return "<i>{datetime}</i><pre>\n{message}</pre>".format(message=record.msg, datetime=t)


def create_logger(process_name):
    logger = logging.getLogger(process_name)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # logging to file
    fh = logging.FileHandler('{}.log'.format(process_name))
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    # logging to console
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # logging to Telegram if token exists
    if os.getenv('TELEGRAM_TOKEN'):
        que = queue.Queue(-1)  # no limit on size
        queue_handler = logging.handlers.QueueHandler(que)
        th = TelegramRequestsHandler()
        listener = logging.handlers.QueueListener(que, th)
        formatter = LogstashFormatter()
        th.setFormatter(formatter)
        logger.addHandler(queue_handler)
        listener.start()

    logger.info('Logger started')
    return logger


logger = create_logger('realestate-review')
