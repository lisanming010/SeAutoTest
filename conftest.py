import pytest
import logging
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

@pytest.fixture(scope="session", autouse=True)
def init_driver():
    edge_options = webdriver.EdgeOptions()

    edge_options.add_argument('--ignore-certificate-errors')  #忽略ssl证书错误
    edge_options.add_argument('--ignore-ssl-errors')
    edge_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Edge(options=edge_options)
    driver.implicitly_wait(10)
    logging.info("driver 初始化成功！")

    yield driver

    driver.close()

@pytest.fixture()
def login(request):
    driver = init_driver()
    logger = init_logger()

    driver.get('https://10.16.204.131')
    elements_selector = LoginPageEles(driver, logger)
    username_input = elements_selector.user_name_input()
    passwd_input = elements_selector.passwd_input()
    login_button = elements_selector.login_button()
    ActionChains(driver).click(username_input).send_keys('admin').click(passwd_input).send_keys('Pass@admin2024').click(login_button).perform()
    sleep(10)
    return driver, logger