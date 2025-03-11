from selenium.webdriver.common.by import By
from pages_selector import exception_handling
from pages_selector.page_index import IndexHeadMenu

class ComputeHeadMenu(IndexHeadMenu):
    def __init__(self, driver, logger):
        '''
        计算页面上方菜单列表，虚拟机、虚拟机分组、模板、镜像、备份、导出文件
        '''
        super().__init__(driver, logger)
    
    # def __init__(self, driver, logger):
    #     '''
    #     计算页面上方菜单列表，虚拟机、虚拟机分组、模板、镜像、备份、导出文件
    #     '''
    #     self.driver = driver
    #     self.logger = logger

    @exception_handling.ele_selector_exception_handing
    def instance_button(self):
        instance_button = self.driver.find_element(By.XPATH, "//div[@class='i-header-submenu']//span[text()='虚拟机']")
        return instance_button
    
    @exception_handling.ele_selector_exception_handing
    def resource_group_button(self):
        resource_group_button = self.driver.find_element(By.XPATH, "//div[@class='i-header-submenu']//span[text()='虚拟机分组']")
        return resource_group_button
    
    @exception_handling.ele_selector_exception_handing
    def vm_template_button(self):
        vm_template_button = self.driver.find_element(By.XPATH, "//div[@class='i-header-submenu']//span[text()='模板']")
        return vm_template_button
    
    @exception_handling.ele_selector_exception_handing
    def file_iso_button(self):
        file_iso_button = self.driver.find_element(By.XPATH, "//div[@class='i-header-submenu']//span[text()='镜像']")
        return file_iso_button

    @exception_handling.ele_selector_exception_handing
    def instance_backup_button(self):
        instance_backup_button = self.driver.find_element(By.XPATH, "//div[@class='i-header-submenu']//span[text()='备份']")
        return instance_backup_button
    
    @exception_handling.ele_selector_exception_handing
    def export_file_button(self):
        export_file_button = self.driver.find_element(By.XPATH, "//div[@class='i-header-submenu']//span[text()='导出文件']")
        return export_file_button
        
class InstancePageEles(ComputeHeadMenu):
    def __init__(self, driver, logger):
        '''
        虚拟机页面操作按钮选择
        '''
        super().__init__(driver, logger)

    @exception_handling.ele_selector_exception_handing
    def create_vm_button(self):
        create_vm_button = self.driver.find_element(By.XPATH, "//span[text()='创建虚拟机']")
        return create_vm_button
    
    @exception_handling.ele_selector_exception_handing
    def vm_on_head_button(self):
        vm_on_head_button = self.driver.find_element(By.XPATH, "//span[text()='开机']")
        return vm_on_head_button
    
    @exception_handling.ele_selector_exception_handing
    def vm_shutdown_head_button(self):
        vm_shutdown_head_button = self.driver.find_element(By.XPATH, "//span[text()='关机']")
        return vm_shutdown_head_button
    
    @exception_handling.ele_selector_exception_handing
    def more_action_head_button(self):
        more_action_head_button = self.driver.find_element(By.XPATH, "//span[text()=' 更多操作 ']")
        return more_action_head_button
    
    @exception_handling.ele_selector_exception_handing
    def reboot_more_act_button(self):
        '''
        列表上方更多操作展开菜单中，需要先选中虚拟机记录并点击更多操作按钮
        '''
        reboot_more_act_button = self.driver.find_element(By.XPATH, "//div[@x-placement='bottom']//li[text()='重启 ']")
        return reboot_more_act_button
    
    @exception_handling.ele_selector_exception_handing
    def remote_login_head_button(self):
        '''
        列表上方更多操作展开菜单中，需要先选中虚拟机记录并点击更多操作按钮
        '''
        remote_login_head_button = self.driver.find_element(By.XPATH, "//div[@x-placement='bottom']//li[text()='远程登录']")
        return remote_login_head_button

    @exception_handling.ele_selector_exception_handing
    def remote_vnc_head_button(self):
        '''
        列表上方更多操作展开菜单中，选中开机状态的虚拟机-更多操作-远程登陆-控制台VNC
        '''
        remote_vnc_head_button = self.driver.find_element(By.XPATH, "//div[@x-placement='right']//li[text()=' 控制台-VNC ']")
        return remote_vnc_head_button
    
class InstanceList(InstancePageEles):
    def __init__(self, driver, logger):
        '''
        虚拟机列表操作验证
        '''
        super().__init__(driver, logger)

    @exception_handling.ele_selector_exception_handing
    def select_vm_list(self, row_id):
        # select_vm_list = self.driver.find_element(By.XPATH, f"//tr[@rowid='i-005d26e5d2']//span[@class='vxe-cell--checkbox']")
        select_vm_list = self.driver.find_element(By.XPATH, f"//tr[@rowid='{row_id}']")
        return select_vm_list