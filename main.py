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

def init_conf_hadler():
    conf_handler = HandleConfig('setting.ini')
    return conf_handler

def make_pytest_conf():
    conf_hadler = init_conf_hadler()
    conf_hadler.conf_write()

if __name__ == '__main__':
    make_pytest_conf()
    pytest.main()
