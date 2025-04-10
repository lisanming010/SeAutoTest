from logging import Logger
import allure
import pytest
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.edge.webdriver import WebDriver
from pages_selector.find_element import FindEles
from time import sleep


# def test_run(login_driver):
#     driver, logger = login_driver

#     elements_selector = FindEles(driver, logger)
    
#     comput_button = elements_selector.compute_button()
#     ActionChains(driver).click(comput_button).perform()
#     vm_list = elements_selector.select_vm_list('i-005d26e5d2')
#     ActionChains(driver).move_to_element(vm_list).click(vm_list).perform()
#     more_act = elements_selector.more_action_head_button()
#     more_act.click()
#     remote_login = elements_selector.remote_login_head_button()
#     ActionChains(driver).move_to_element(remote_login).perform()
#     remote_login_vnc = elements_selector.remote_vnc_head_button()
#     remote_login_vnc.click()
#     sleep(10)


vm_create_conf = {
    'dirver': 'dirver',
    'logger': 'logger',
    'vmconf': {
        'create_vm_method': '<全新虚拟机>',
        'vm_name': 'SeTestCreate',
        'vcluster': '<x86默认集群>',
        'group_name': '<默认分组>',
        'storage_pool_name': '<本地存储池-10.16.204.135-sdc>',
        'schedule_type': '<指定主机>',
        'host_ip': '<10.16.204.125>',
        'auto_start': True,
        'system_type': '<Windows>',
        'boot_type': '<UEFI>',
        'remark': '测试备注',
        'cpu_core_num': '4',
        'cpu_socket_num': '<2>',
        'memory_size': '4',
        'vm_disk_num': 1,
        'vm_disk1': {
            'disk_size': '100',
        },
        'vm_nic_num': 1,
        'vm_nic1':{
            'uplink_switch_name': '<外部交换机>',
            'mac_addr': '<d0:0d:44:3b:c7:99>',
            'firewall_name': '<测试防火墙>',
            'is_use_ipv4': True,
            'ipv4_addr': '<10.16.204.175>',
            'ipv4_prefix': '<255.255.248.0>',
            'ipv4_gateway': '<10.16.207.254>',
            'is_online': True,
            'is_ipcheck': True,
            'in_bandwidth': '20',
            'out_bandwidth': '25',
            'vnic_queue': '',
        }
    },
}



def vm_create_dict_setup():
    vm_create_conf = {}
    return vm_create_conf

@allure.feature('虚拟机创建')
class TestVmCreate():

    @pytest.mark.parametrize('create_vm', vm_create_dict_setup(), indirect=True)
    @allure.story('创建全新虚拟机')
    def test_createvm001_new(slef, login_driver, create_vm):
        driver, logger = login_driver


    
    @allure.story('从模板创建虚拟机')
    def test_createvm002_temp(self, login_driver, create_vm):
        pass