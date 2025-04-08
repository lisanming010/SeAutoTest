import os
from selenium.webdriver.common.by import By
from pages_selector import exception_handling
from utils.confing_handle import HandleConfig

class FindEles:
    def __init__(self, driver, logger):
        """
        :driver: 已请求登陆页面的webdriver 
        :logger: 已完成初始化的logger记录器       
        """
        self.driver = driver
        self.logger = logger
    
    def _get_file_path(self):
        """
        获取文件所处目录
        """
        curr_file_path = os.path.abspath(__file__)
        curr_dir_name = os.path.dirname(curr_file_path)
        return curr_dir_name

    def _config_handler(self):
        """
        设置配置文件读取
        """
        conf_path = os.path.join(self._get_file_path(), 'element_locating.ini') #配置文件路径拼接
        if not os.path.exists(conf_path):
            self.logger.error('element_locating.ini配置文件不存在')
            raise FileNotFoundError
        conf_handler = HandleConfig(conf_path)
        return conf_handler

    @exception_handling.ele_selector_exception_handing
    def find_eles(self, page_local, ele_name, ele_find_by='XPATH'):
        """
        选择元素，返回元素选择器

        :page_local: 元素所处页面，需要与element_locating.ini中section对应
        :ele_name: 元素名称，需要与element_locating.ini中元素option对应
        :ele_find_by: 元素定位方式默认为xpath，需要与element_locating.ini中元素option对应，不指定时默认使用ele_name+find_by拼接
        """
        conf_handler = self._config_handler()
        if conf_handler.has_option(page_local, f'{ele_name}_find_by'):
            ele_find_by = conf_handler.get_value_str(page_local, f'{ele_name}_find_by')
        if ele_find_by == "XPATH": #TODO：根据后续实际需求添加其他定位方式
            ele_find_path = conf_handler.get_value_str(page_local, ele_name)
            ele = self.driver.find_element(By.XPATH, ele_find_path)
            return ele, ele_name
        else:
            raise ('未定义的定位方式')

