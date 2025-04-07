import pytest
from selenium.webdriver.common.action_chains import ActionChains
from pages_selector.find_element import FindEles
from time import sleep
from utils.confing_handle import HandleConfig

def test_run(driver_init):
    conf_handler = HandleConfig('setting.ini')
    env_url = conf_handler.get_value_str('env', 'env_url')
    username = conf_handler.get_value_str('env', 'username')
    passwd = conf_handler.get_value_str('env', 'password')

    driver , logger= driver_init
    driver.get(env_url)
    # elements_selector = LoginPageEles(driver, logger)
    elements_selector = FindEles(driver, logger)
    # username_input = elements_selector.user_name_input()
    # passwd_input = elements_selector.passwd_input()
    # login_button = elements_selector.login_button()
    username_input = elements_selector.find_eles('login', 'username_input')
    passwd_input = elements_selector.find_eles('login', 'password_input')
    login_button = elements_selector.find_eles('login', 'login_button')
    ActionChains(driver).click(username_input)\
        .send_keys(username).click(passwd_input)\
        .send_keys(passwd).click(login_button)\
        .perform()
    