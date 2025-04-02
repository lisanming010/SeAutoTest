import configparser
import ast
import os

class HandleConfig:
    def __init__(self, filename):
        if os.path.exists(filename):
            self.filename = filename
            self.conf = configparser.RawConfigParser()
            self.conf.read(self.filename, encoding='UTF-8')
        else:
            raise FileNotFoundError('文件不存在！')

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
    
    def conf_write(self, conf_file_name='pytest.ini', section='pytest'):
        '''
        从setting中提取pytest section生成新pytest.ini配置文件

        : conf_file_name 新配置文件名称
        : section setting文件中section区域
        '''
        conf_new= configparser.RawConfigParser()
        optins = self.read_section(section)
        conf_new.add_section(section)
        for option, value in optins:
            conf_new.set(section, option, value)

        if os.path.exists(conf_file_name):
            os.remove(conf_file_name)
        with open(conf_file_name, 'x') as f:
            conf_new.write(f)