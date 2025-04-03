import requests
import warnings
import pytest
from selenium import webdriver
from multiprocessing import Process, Pool
from utils.log_handle.log_handle import LoggerSetUp
from utils.confing_handle import HandleConfig
from test_cases.login_test import test_login
from test_cases.vm_test import test_vm_create
from requests.packages import urllib3

SETTIGN_FILE = 'setting.ini'

def make_pytest_conf():
    pytest_conf = HandleConfig(SETTIGN_FILE).read_section('pytest')
    HandleConfig('pytest.ini').conf_write('pytest', pytest_conf)

def update_pytest_conf():
    run_nums = HandleConfig(SETTIGN_FILE).get_value_str('global', 'number_of_process')
    pytest_addopts = HandleConfig(SETTIGN_FILE).get_value_str('pytest', 'addopts')
    value = pytest_addopts + f' -n {run_nums}'
    options = [('addopts', value)]
    HandleConfig('pytest.ini').update_conf('pytest', options)

if __name__ == '__main__':
    make_pytest_conf()
    update_pytest_conf()
    pytest.main()
