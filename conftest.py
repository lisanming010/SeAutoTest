import pytest
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from pages_selector.page_login import LoginPageEles
from utils.log_handle.log_handle import LoggerSetUp

def init_logger():
    logger = LoggerSetUp('test_log_pytest')
    logger.get_conf()
    logger = logger.logger()
    return logger

_driver = ''
_logger = init_logger()

@pytest.fixture(scope="function")
def driver_init():
    global _driver, _logger
    _logger.info("开始初始化WebDriver...")
    
    edge_options = webdriver.EdgeOptions()
    edge_options.add_argument('--ignore-certificate-errors')
    edge_options.add_argument('--ignore-ssl-errors')
    edge_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    _driver = webdriver.Edge(options=edge_options)
    _driver.implicitly_wait(10)
    _logger.info("WebDriver初始化成功！")

    yield _driver, _logger  # 返回driver对象

    # 释放webdriver
    _logger.info("关闭WebDriver...")
    _driver.close()

@pytest.fixture(scope="function")
def login_driver(driver_init):
    global _driver, _logger
    if _driver == '':        # 避免重复初始化webdriver
        _driver, _ = driver_init   
    
    try:
        _driver.get('https://10.16.204.131')
        elements_selector = LoginPageEles(_driver, _logger)
        username_input = elements_selector.user_name_input()
        passwd_input = elements_selector.passwd_input()
        login_button = elements_selector.login_button()
        
        ActionChains(_driver).click(username_input)\
            .send_keys('admin')\
            .click(passwd_input)\
            .send_keys('Pass@admin2024')\
            .click(login_button)\
            .perform()
        
        sleep(3)
        _logger.info("登录成功")
        
    except Exception as e:
        _logger.error(f"登录失败: {str(e)}")
        raise e

    return _driver, _logger