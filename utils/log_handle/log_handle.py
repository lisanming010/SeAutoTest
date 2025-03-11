import logging, os
from logging.config import dictConfig
from utils.log_handle.log_config import log_conf_dict

class LoggerSetUp:
    def __init__(self, log_file_name, log_file_path=''):
        curr_path = os.path.dirname(os.path.abspath(__file__))
        log_dir_name = os.path.join(curr_path, '..', '..', 'logs')
        log_file_path = log_dir_name

        self.log_file_name = log_file_name
        self.log_file_path = log_file_path

    def get_conf(self):
        '''
        应用日志配置文件
        '''
        log_config_dict = log_conf_dict(self.log_file_name, self.log_file_path)
        dictConfig(log_config_dict)

    def logger(self):
        '''
        实例化日志记录器
        '''
        logger = logging.getLogger(self.log_file_name)
        return logger
