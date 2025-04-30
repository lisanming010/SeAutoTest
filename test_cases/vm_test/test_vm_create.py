import allure
import pytest
from time import sleep
from assert_check import AssertCheck

vm_create_conf = {
    'vmconf': {
        'create_vm_method': '<全新虚拟机>',
        'vm_temp_id': '<vmt-005363c8ae>',
        'vm_temp_name': '<OE2203SP1>', 
        'vm_name': 'SeTestCreate',
        'vcluster': '<Aarch64默认集群>',
        'group_name': '<默认分组>',
        'storage_pool_name': '<ceph_1>',
        'schedule_type': '<指定主机>',
        'host_ip': '<10.16.221.155>',
        'auto_start': True,
        'system_type': '<Windows>',
        'boot_type': '<UEFI>',
        'remark': '测试备注',
        'cpu_core_num': '4',
        'cpu_socket_num': '',
        'memory_size': '4',
        'vm_disk_num': 1,
        'vm_disk1': {
            'disk_size': '100'
        },
        'vm_nic_num': 1,
        'vm_nic1':{
            'uplink_switch_name': '<内部交换机123>',
            'mac_addr': 'd0:0d:44:3b:c7:89',
            'firewall_name': '',
            'is_use_ipv4': True,
            'ipv4_addr': '192.168.30.100',
            'ipv4_prefix': '',
            'ipv4_gateway': '',
            'is_online': True,
            'is_ipcheck': True,
            'in_bandwidth': '20',
            'out_bandwidth': '25',
            'vnic_queue': ''
        },
        'iso_num': 1,
        'iso1': {
            'is_external_iso': False,
            'iso_name_or_link': '<openEuler-22.03-LTS-SP1-aarch64-dvd.iso>',
            'iso_file_id': '<file-00c1c237d7>',
            'associated_storage_pool': '<ceph_1>'
        },
        'usb_num': 1,
        'usb1': '',
        'vm_create_num': 1
    }
}

@allure.feature('虚拟机创建')
class TestVmCreate():

    @pytest.mark.parametrize('create_vm', [vm_create_conf], indirect=True)
    @allure.story('创建全新虚拟机')
    def test_createvm001_new(slef, create_vm):
        driver, logger = create_vm
        assert_check = AssertCheck(driver, logger, vm_create_conf).vm_hw_conf_check()
        assert assert_check == 1