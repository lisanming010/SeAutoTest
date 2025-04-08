import allure
from selenium.webdriver.common.action_chains import ActionChains
from pages_selector.find_element import FindEles
from time import sleep


# def test_run(login_driver):
#     driver, logger = login_driver

#     elements_selector = FindEles(driver, logger)
    
#     comput_button = elements_selector.compute_button()
#     ActionChains(driver).click(comput_button).perform()
#     vm_list = elements_selector.select_vm_list('i-005d26e5d2')
#     ActionChains(driver).move_to_element(vm_list).click(vm_list).perform()
#     more_act = elements_selector.more_action_head_button()
#     more_act.click()
#     remote_login = elements_selector.remote_login_head_button()
#     ActionChains(driver).move_to_element(remote_login).perform()
#     remote_login_vnc = elements_selector.remote_vnc_head_button()
#     remote_login_vnc.click()
#     sleep(10)

class TestVmCreate():

    def test_createvm001_new(slef, login_driver):
        driver, logger = login_driver

        # elements_selector = FindEles(driver, logger)
        
        # comput_button = elements_selector.find_eles('page_head_index', 'compute_button')
        # ActionChains(driver).click(comput_button).perform()
        sleep(3)
        # vm_list = elements_selector.select_vm_list('i-005d26e5d2')
        # ActionChains(driver).move_to_element(vm_list).click(vm_list).perform()
        # more_act = elements_selector.more_action_head_button()
        # more_act.click()
        # remote_login = elements_selector.remote_login_head_button()
        # ActionChains(driver).move_to_element(remote_login).perform()
        # remote_login_vnc = elements_selector.remote_vnc_head_button()
        # remote_login_vnc.click()
        # sleep(10)
    
    def test_createvm002_temp(self, login_driver):
        pass