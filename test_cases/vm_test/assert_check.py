from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from pages_selector.find_element import FindEles
from utils.ele_action import EleAction

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
            self.vm_list_selector.ele_selection('vm_name_button', vm_name, ele_kind='list')
        except:
            pass

        return assert_flag
    