import configparser
import ast

class HandleConfig:
    def __init__(self, filename):
        self.filename = filename
        self.conf = configparser.ConfigParser()
        self.conf.read(self.filename, encoding='UTF-8')

    def get_value_str(self, section, optinon):
        return self.conf.get(section, optinon)
    
    def get_int(self, section, option):
        return self.conf.getint(section, option)
    
    def get_bool(self, section, option):
        return self.conf.getboolean(section, option)
    
    def get_eval_data(self, section, option):
        return ast.literal_eval(self.conf.get(section, option))