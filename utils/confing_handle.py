import configparser
import ast
import os

class HandleConfig:
    def __init__(self, filename):
        self.filename = filename
        self.conf = configparser.RawConfigParser()
        if os.path.exists(filename):
            self.conf.read(self.filename, encoding='UTF-8')

    def read_section(self, section):
        return self.conf.items(section)

    def get_value_str(self, section, option):
        return self.conf.get(section, option)
            
    def get_int(self, section, option):
        return self.conf.getint(section, option)
    
    def get_bool(self, section, option):
        return self.conf.getboolean(section, option)
    
    def get_eval_data(self, section, option):
        return ast.literal_eval(self.conf.get(section, option))
    
    def conf_write(self, section, options):
        
        if self.conf.has_section(section):
            self.conf.remove_section(section)
        self.conf.add_section(section)
        for option, value in options:
            self.conf.set(section, option, value)

        with open(self.filename, 'w') as f:
            self.conf.write(f)

    def update_conf(self, section, options):
        
        if not self.conf.has_section(section):
            self.conf.add_section(section)
        for option, value in options:
            if self.conf.has_option(section, option):
                self.conf.remove_option(section, option)
            self.conf.set(section, option, value)

        with open(self.filename, 'w') as f:
            self.conf.write(f)
