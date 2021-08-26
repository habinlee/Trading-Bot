import sys
import time
import datetime
import logging
import logging.handlers
import subprocess
from datetime import datetime,timedelta
import pytz
from pytz import timezone, utc
import os

class LoggerFile:
    def __init__(self):
        self.time_now = time.strftime('%Y-%m-%d %X', time.localtime(time.time()))

        self.current_dir = os.path.dirname(os.path.realpath(__file__))
        self.current_file = os.path.basename(__file__)[:-3] #xxxx.py

        self.local_tz = pytz.timezone('Asia/Seoul')

    def localTime(self, *args):
        utc_dt = utc.localize(datetime.utcnow())
        converted = utc_dt.astimezone(self.local_tz)

        return converted.timetuple()

    def make_dir(self):
        log_dir = '{}/logs'.format(self.current_dir)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        return log_dir

    def logging(self):
        log_dir = self.make_dir()
        LOG_FILENAME = '{}/log_{}'.format(log_dir, self.current_file)
        logger = logging.getLogger(self.current_file)
        logger.setLevel(logging.DEBUG)
        file_handler = logging.handlers.TimedRotatingFileHandler(LOG_FILENAME, when='midnight', interval=1, backupCount=14)
        file_handler.suffix = 'log-%Y%m%d'
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(process)d - [%(filename)s:%(lineno)d] %(message)s')
        formatter.converter = self.localTime
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        return logger

    def prevent_reload(self):
        result = subprocess.check_output('ps -ef | grep {} | wc -l'.format(os.path.basename(__file__)), shell=True)
        if int(result.strip()) > 3:
            print('There is a previous run; I \'m exiting')
            sys.exit(0)