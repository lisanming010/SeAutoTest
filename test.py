from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from pages_selector.page_login import LoginPageEles
from utils.log_handle.log_handle import LoggerSetUp
from utils.confing_handle import HandleConfig


# logger = LoggerSetUp('test_log_pytest')
# logger.get_conf()
# logger = logger.logger()

# edge_options = webdriver.EdgeOptions()
# edge_options.add_argument('--ignore-certificate-errors')
# edge_options.add_argument('--ignore-ssl-errors')
# edge_options.add_experimental_option('excludeSwitches', ['enable-logging'])
# driver = webdriver.Edge(options=edge_options)
# driver.implicitly_wait(10)

# driver.get('https://10.16.204.131')

# elements_selector = LoginPageEles(driver, logger)
# username_input = elements_selector.user_name_input()
# passwd_input = elements_selector.passwd_input()
# login_button = elements_selector.login_button()
# ActionChains(driver).click(username_input).send_keys('admin').click(passwd_input).send_keys('Pass@admin2025').click(login_button).perform()
# try:
#     alert = driver.switch_to.alert
#     print(alert.text)
# except Exception as e:
#     print("error")

conf_reader = HandleConfig('setting.ini')
conf_reader.conf_write(conf_file_name='test.ini')