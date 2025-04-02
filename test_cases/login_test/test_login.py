import pytest
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from pages_selector.page_login import LoginPageEles
from time import sleep

def test_run(driver_init):
    driver , logger= driver_init
    elements_selector = LoginPageEles(driver, logger)
    username_input = elements_selector.user_name_input()
    passwd_input = elements_selector.passwd_input()
    login_button = elements_selector.login_button()
    ActionChains(driver).click(username_input).send_keys('admin').click(passwd_input).send_keys('Pass@admin2024').click(login_button).perform()
    