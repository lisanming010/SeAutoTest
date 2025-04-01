from selenium.webdriver.common.action_chains import ActionChains
from pages_selector.page_compute import *
from pages_selector.page_login import LoginPageEles
from time import sleep

# def run_login(driver, logger):
#     elements_selector = LoginPageEles(driver, logger)
#     username_input = elements_selector.user_name_input()
#     passwd_input = elements_selector.passwd_input()
#     login_button = elements_selector.login_button()
#     ActionChains(driver).click(username_input).send_keys('admin').click(passwd_input).send_keys('Pass@admin2024').click(login_button).perform()

def run_test(driver, logger):
    # run_login(driver, logger)
    elements_selector = InstanceList(driver, logger)
    comput_button = elements_selector.compute_button()
    ActionChains(driver).click(comput_button).perform()
    vm_list = elements_selector.select_vm_list('i-005d26e5d2')
    ActionChains(driver).move_to_element(vm_list).click(vm_list).perform()
    more_act = elements_selector.more_action_head_button()
    more_act.click()
    remote_login = elements_selector.remote_login_head_button()
    ActionChains(driver).move_to_element(remote_login).perform()
    remote_login_vnc = elements_selector.remote_vnc_head_button()
    remote_login_vnc.click()
    sleep(10)