import requests
import warnings
from selenium import webdriver
from multiprocessing import Process, Pool
from utils.log_handle.log_handle import LoggerSetUp
from utils.confing_read import HandleConfig
from test_cases.login_test import test_login
from test_cases.vm_test import test_vm_create
from requests.packages import urllib3

# 关闭警告
urllib3.disable_warnings()
warnings.filterwarnings("ignore")

def driver_set_up(url):
    '''
    webdriver配置，并访问请求网页

    :URL: 网页入口
    '''
    edge_options = webdriver.EdgeOptions()

    edge_options.add_argument('--ignore-certificate-errors')  #忽略ssl证书错误
    edge_options.add_argument('--ignore-ssl-errors')
    edge_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Edge(options=edge_options)

    driver.implicitly_wait(10)
    driver.get(url)
    driver.fullscreen_window()
    return driver

def logger_set_up(logger_name):
    logger = LoggerSetUp(logger_name)
    logger.get_conf()
    logger = logger.logger()
    return logger


headle_config = HandleConfig("setting.ini")
pool_size = headle_config.get_int('global', 'number_of_threads')
url = headle_config.get_value_str('global', 'env_url')
ignore_ssl_error = headle_config.get_bool('global', 'ignore_ssl_error')

driver = driver_set_up(url)


logger = logger_set_up('test_vm')
test_vm_create.run_test(driver, logger)
driver.close()
