from selenium.webdriver.common.by import By
from pages_selector import exception_handling

class IndexHeadMenu:
    def __init__(self, driver, logger):
        '''
        系统最上层菜单列表，首页、计算、存储、网络、主机、vmware、平台管理
        '''
        self.driver = driver
        self.logger = logger

    @exception_handling.ele_selector_exception_handing
    def index_button(self):
        index_button = self.driver.find_element(By.XPATH, "//span[text()='首页']")
        return index_button
    
    @exception_handling.ele_selector_exception_handing
    def compute_button(self):
        compute_button = self.driver.find_element(By.XPATH, "//span[text()='计算']")
        return compute_button
    
    @exception_handling.ele_selector_exception_handing
    def storage_button(self):
        storage_button = self.driver.find_element(By.XPATH, "//span[text()='存储']")
        return storage_button
    
    @exception_handling.ele_selector_exception_handing
    def network_button(self):
        network_button = self.driver.find_element(By.XPATH, "//span[text()='网络']")
        return network_button
    
    @exception_handling.ele_selector_exception_handing
    def physical_button(self):
        physical_button = self.driver.find_element(By.XPATH, "//span[text()='主机']")
        return physical_button
    
    @exception_handling.ele_selector_exception_handing
    def vmware_button(self):
        vmware_button = self.driver.find_element(By.XPATH, "//span[text()='VMware']")
        return vmware_button
    
    @exception_handling.ele_selector_exception_handing
    def system_button(self):
        system_button = self.driver.find_element(By.XPATH, "//span[text()='平台管理']")
        return system_button

class IndexPageEles:
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger

    