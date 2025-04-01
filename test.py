from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import test_cases
import pytest

# edge_options = webdriver.EdgeOptions()
# edge_options.add_argument('--ignore-certificate-errors')
# edge_options.add_argument('--ignore-ssl-errors')
# edge_options.add_experimental_option('excludeSwitches', ['enable-logging'])
# driver = webdriver.Edge(options=edge_options)
# driver.implicitly_wait(10)

# driver.get('https://10.16.204.131')

# username = driver.find_element(By.XPATH, "//input[@name='username']")
# print(username)
# driver.close()

# from multiprocessing import Process, Pool
# from utils.log_handle.log_handle import loggerSetUp

pytest.main()

# def log_out_put(logger_name):
#     logger = loggerSetUp(logger_name)
#     logger.get_conf()
#     logger = logger.logger()
#     logger.error(f'{logger_name}:test error')

# if __name__ == '__main__':
#     pool = Pool(2)
#     for i in range(2):
#         name = f'test_{i}'
#         pool.apply_async(func=log_out_put, args=(name,))

#     pool.close()
#     pool.join()

# class testClass:
#     test1 = ''
#     def __init__(self):
#         self.test1 = 'test1'
        
#     def print_test(self):
#         print(self.test1)

# test = testClass()
# test.print_test()