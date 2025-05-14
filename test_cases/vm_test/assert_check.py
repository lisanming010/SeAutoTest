from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from pages_selector.find_element import FindEles
from utils.ele_action import EleAction
from time import sleep
import selenium.common.exceptions as seEception

class AssertCheck():
    def __init__(self, driver, logger, vm_conf):
        self.driver = driver
        self.logger = logger
        self.vm_conf = vm_conf
        
        ele_find = FindEles(self.driver, self.logger)
        self.vm_list_selector = EleAction(self.driver, ele_find, 'vm_list', self.logger)
        self.vmconf_details_page_selector = EleAction(self.driver, ele_find, 'vm_hw_conf_details', self.logger)

    def vm_create_hw_conf_check(self):
        assert_flag = 1
        
        vm_name = self.vm_conf['vm_name']
        try:
            vm_name_button = self.vm_list_selector.ele_selection('vm_name_button', vm_name, ele_kind='list')
        except seEception.NoSuchElementException: # 查找不到虚拟机记录，判断为创建失败。TODO：添加日志采集输出错误详情，看是用se还是走接口
            assert_flag = 0
        else:
            '''运行状态判断'''
            vm_id_ele = self.vm_list_selector.ele_selection('vm_id', vm_name)
            vm_line_text = vm_id_ele.text.strip().split('\n') #输出对应虚拟机整列text，ID、名称、状态、IP地址、规格、主机、创建人
            vm_id = vm_line_text[0]
            while True:
                sleep(3)
                vm_statu = self.vm_list_selector.ele_selection('vm_stat', vm_id).text.strip()
                if self.vm_conf['auto_start']:
                    if '已关机' in vm_statu:
                        assert_flag = 0
                    elif '运行中' in vm_statu:
                        assert_flag = 0
                        break
                else:
                    if '已关机' in vm_statu:
                        break
            
            '''所属节点判断'''

        return assert_flag
    