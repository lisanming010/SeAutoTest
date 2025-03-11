from selenium.webdriver.common.by import By
from pages_selector import exception_handling

class LoginPageEles:
    def __init__(self, driver, logger):
        '''
        登陆页面元素选择类

        :driver: 已请求登陆页面的webdriver 
        :logger: 已完成初始化的logger记录器
        '''
        self.driver = driver
        self.logger = logger
        
    @exception_handling.ele_selector_exception_handing
    def user_name_input(self):
        username = self.driver.find_element(By.XPATH, "//input[@name='username']")
        return username

    @exception_handling.ele_selector_exception_handing
    def passwd_input(self):
        passwd = self.driver.find_element(By.XPATH, "//input[@name='password']")
        return passwd
    
    @exception_handling.ele_selector_exception_handing
    def login_button(self):
        login_button = self.driver.find_element(By.XPATH, "//span[text()='登录 ']")
        return login_button