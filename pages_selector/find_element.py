import os
from selenium.webdriver.common.by import By
from pages_selector import exception_handling
from utils.confing_handle import HandleConfig
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

    def config_handler(self):
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
    def find_ele(self, page_local, ele_name, ele_find_by='XPATH', replace_target='', find_list=False):
        """
        选择元素，返回元素选择器

        :page_local: 元素所处页面，需要与element_locating.ini中section对应
        :ele_name: 元素名称，需要与element_locating.ini中元素option对应
        :ele_find_by: 元素定位方式默认为xpath，需要与element_locating.ini中元素option对应，不指定时默认使用ele_name+find_by拼接
        :replace_str: 替换定位xpath部分内容，默认为空不执行替换，传递list时将会遍历list执行替换
        :find_list: True:find_element,false:find_elements,默认为false
        """
        conf_handler = self.config_handler()
        if conf_handler.has_option(page_local, f'{ele_name}_find_by'):
            ele_find_by = conf_handler.get_value_str(page_local, f'{ele_name}_find_by')

        if ele_find_by == "XPATH": #TODO：根据后续实际需求添加其他定位方式
            ele_find_path = conf_handler.get_value_str(page_local, ele_name)
            if replace_target != '' :
                if type(replace_target) is str:  #处理多项替换
                    replace_target = replace_target.strip('<>')
                    ele_find_path = ele_find_path.replace('<replace>', replace_target)

                elif type(replace_target) is list:
                    for i in replace_target:
                        i = i.strip('<>')
                        ele_find_path = ele_find_path.replace('<replace>', i, 1)

            if find_list:
                ele = self.driver.find_elements(By.XPATH, ele_find_path)
            else:            
                ele = self.driver.find_element(By.XPATH, ele_find_path)
            return ele, ele_name
        else:
            raise NameError(f'未定义的定位方式{ele_find_by}')
        
    @exception_handling.ele_selector_exception_handing
    def find_ele_base_ele(self, ele, by, follow_path, find_list=False):
        '''
        webelement对象方法封装，支持从当前ele对象路径下再次检索

        :ele: 起始元素
        :by: 定位方式，目前仅支持xpath
        :follow_path: 定位路径
        :find_list: 是否定位多个元素，即是否调用find_elements
        ——> ele
        '''
        if by == 'xpath':
            if find_list:
                ele = ele.find_elements(By.XPATH, follow_path)
            else:
                ele = ele.find_element(By.XPATH, follow_path)
        else:
            raise RuntimeError(f'未定义的定位方式{by}')
        return ele, str(ele)
        
