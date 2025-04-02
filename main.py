import requests
import warnings
import pytest
from selenium import webdriver
from multiprocessing import Process, Pool
from utils.log_handle.log_handle import LoggerSetUp
from utils.confing_read import HandleConfig
from test_cases.login_test import test_login
from test_cases.vm_test import test_vm_create
from requests.packages import urllib3

pytest.main()
