import pytest
import os
import time
import allure
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from utils.log_handle.log_handle import LoggerSetUp
from config import cfg_global
from pages_selector.find_element import FindEles
from utils.tools import OtherTools

_driver = ''
_conf_handler = cfg_global

def init_logger():
    logger = LoggerSetUp('test_log_pytest')
    logger.get_conf()
    logger = logger.logger()
    return logger

_logger = init_logger()

@pytest.fixture(scope="class")
def driver_init():
    global _driver, _logger
    _logger.info("开始初始化WebDriver...")
    
    edge_options = webdriver.EdgeOptions()
    if _conf_handler.get_bool('global', 'ignore_ssl_error'):
        edge_options.add_argument('--ignore-certificate-errors')
        edge_options.add_argument('--ignore-ssl-errors')
    edge_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    _driver = webdriver.Edge(options=edge_options)
    # _driver.implicitly_wait(10)
    _driver.maximize_window()
    _logger.info("WebDriver初始化成功！")

    yield _driver, _logger  # 返回driver对象

    # 释放webdriver
    _logger.info("关闭WebDriver...")
    _driver.close()

@pytest.fixture()
def login_driver(driver_init):
    global _driver, _logger
    if _driver == '':        # 避免重复初始化webdriver
        _driver, _ = driver_init   
    
    env_url = _conf_handler.get_value_str('env', 'env_url')
    username = _conf_handler.get_value_str('env', 'username')
    passwd = _conf_handler.get_value_str('env', 'password')
    _driver.get(env_url)
    elements_selector = FindEles(_driver, _logger)

    try: # 登入环境
        username_input = elements_selector.find_ele('login', 'username_input')
        passwd_input = elements_selector.find_ele('login', 'password_input')
        login_button = elements_selector.find_ele('login', 'login_button')
        ActionChains(_driver).click(username_input)\
            .send_keys(username)\
            .click(passwd_input)\
            .send_keys(passwd)\
            .click(login_button)\
            .perform()
        sleep(3)
        _logger.info("登录成功")
        
    except Exception as e:
        _logger.error(f"登录失败: {str(e)}")
        raise e

    yield _driver, _logger

    # try: # teardown 登出系统
    #     user_info_ele = elements_selector.find_ele('page_head_index', 'head_user_info')
    #     ActionChains(_driver).move_to_element(user_info_ele).perform()
    #     logout = elements_selector.find_ele('page_head_index', 'head_user_info_logout')
    #     ActionChains(_driver).click(logout).perform()
    #     _logger.info("退出登陆成功！")
        
    # except Exception as e:
    #     _logger.error(f"退出登陆失败：{str(e)}")
    #     raise e

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    outcom = yield
    rep = outcom.get_result()
    if rep.when == 'call' and rep.failed:
        test_name = item.name
        if _driver:
            screenshoot_path = OtherTools.screen_shot(_driver, test_name)
            allure.attach.file(screenshoot_path, name='ScreenShot', 
                               attachment_type=allure.attachment_type.PNG)