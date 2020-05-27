import logging
import os
import datetime
from Utils.Settings import Config

class Logger(logging.Logger):

    file_format = '%(asctime)s.%(msecs)3d %(levelname)-8s %(module)s - %(funcName)s: %(message)s'
    console_format = '%(asctime)s %(levelname)-8s %(name)-12s: %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    path = "Logs/"

    def __init__(self, name,file_path=None,log_level=logging.INFO,log_console=True):
        if not file_path:
            file_path = Logger.path
        if not os.path.exists(file_path):
            os.makedirs(file_path)

        logging.Logger.__init__(self,name)
        run_time = datetime.datetime.now().strftime("%d-%m__%H-%M-%S")
        logging.basicConfig(
            filename='{}/{}__{}'.format(file_path, name, run_time),
            level=log_level,
            format=Logger.file_format,
            datefmt=Logger.date_format)

        if log_console:
            console = logging.StreamHandler()
            console.setLevel(logging.INFO)
            formatter = logging.Formatter(Logger.console_format)
            # tell the handler to use this format
            console.setFormatter(formatter)
            logging.Logger.addHandler(self,console)