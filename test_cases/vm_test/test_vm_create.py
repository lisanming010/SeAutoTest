import allure
import pytest
from time import sleep
from test_cases.vm_test.vm_assert_check import AssertCheck

vm_create_conf = {
    'vmconf': {
        'create_vm_method': '<全新虚拟机>',
        'vm_temp_id': '<vmt-00bd35358e>',
        'vm_temp_name': '<OE2203SP1-x86-uefi>', 
        'vm_name': 'SeTestCreate',
        'vcluster': '<X86默认集群>',
        'group_name': '<默认分组>',
        'storage_pool_name': '<san2>',
        'schedule_type': '<指定主机>',
        'host_ip': '<10.16.221.4>',
        'auto_start': True,
        'system_type': '<Windows>',
        'boot_type': '<UEFI>',
        'remark': '测试备注',
        'cpu_core_num': '1',
        'cpu_socket_num': '',
        'memory_size': '1',
        'vm_disk_num': 1,
        'vm_disk1': {
            'disk_size': '100'
        },
        'vm_nic_num': 2,
        'vm_nic1':{
            'uplink_switch_name': '<测试双栈交换机>',
            'mac_addr': 'd0:0d:44:3b:c7:89',
            'firewall_name': '',
            'is_use_ipv4': True,
            'ipv4_addr': '192.168.221.100',
            'ipv4_prefix': '255.255.255.0',
            'ipv4_gateway': '192.168.221.254',
            'ipv4_subip_is_use': True,
            'ipv4_subip_set_mode': '指定',
            'ipv4_subip_random_nums': 2,
            'ipv4_subip_appoint_addr': '192.168.221.101-192.168.221.103',
            'is_use_ipv6': True,
            'ipv6_addr': 'fd77:aa1::aac',
            'ipv6_prefix': 'ffff:ffff:ffff:ffff::',
            'ipv6_gateway': 'fd77:aa1::1',
            'ipv6_subip_is_use': True,
            'ipv6_subip_set_mode': '指定',
            'ipv6_subip_random_nums': 2,
            'ipv6_subip_appoint_addr': 'fd77:aa1::101',
            'is_online': True,
            'is_ipcheck': True,
            'in_bandwidth': '20',
            'out_bandwidth': '25',
            'vnic_queue': ''
        },
        'vm_nic2':{
            'uplink_switch_name': '<测试双栈交换机>',
            'mac_addr': 'd0:0d:44:3b:c7:90',
            'firewall_name': '',
            'is_use_ipv4': True,
            'ipv4_addr': '192.168.221.105',
            'ipv4_prefix': '255.255.255.0',
            'ipv4_gateway': '192.168.221.254',
            'ipv4_subip_is_use': True,
            'ipv4_subip_set_mode': '指定',
            'ipv4_subip_random_nums': 2,
            'ipv4_subip_appoint_addr': '192.168.221.106-192.168.221.108',
            'is_use_ipv6': True,
            'ipv6_addr': 'fd77:aa1::aaa',
            'ipv6_prefix': 'ffff:ffff:ffff:ffff::',
            'ipv6_gateway': 'fd77:aa1::1',
            'ipv6_subip_is_use': True,
            'ipv6_subip_set_mode': '指定',
            'ipv6_subip_random_nums': 2,
            'ipv6_subip_appoint_addr': 'fd77:aa1::102',
            'is_online': True,
            'is_ipcheck': True,
            'in_bandwidth': '20',
            'out_bandwidth': '25',
            'vnic_queue': ''
        },
        'iso_num': 1,
        'iso1': {
            'is_external_iso': False,
            'iso_name_or_link': '<Kylin-Server-V10-SP3-2403-Release-20240426-X86_64.iso>',
            'iso_file_id': '<file-0011e216cf>',
            'associated_storage_pool': '<san1>'
        },
        'usb_num': 0,
        'usb1': '',
        'vm_create_num': 1
    }
}

@allure.feature('虚拟机创建')
class TestVmCreate:

    @pytest.mark.parametrize('create_vm', [vm_create_conf], indirect=True)
    @allure.story('创建全新虚拟机')
    def test_createvm001_new(self, create_vm):
        driver, logger, _ = create_vm
        assert_check = AssertCheck(driver, logger, vm_create_conf['vmconf']).vm_create_hw_conf_check()
        assert assert_check == 1

    # @pytest.mark.parametrize('create_vm', [vm_create_conf], indirect=True)
    # @allure.story('从模板创建虚拟机')
    # def test_createvm002_from_temp(self, create_vm):
    #     pass

    # @pytest.mark.parametrize('create_vm', [vm_create_conf], indirect=True)
    # @allure.story('从备份创建虚拟机')
    # def test_createvm002_from_backup(self, create_vm):
    #     pass

    # @pytest.mark.parametrize('create_vm', [vm_create_conf], indirect=True)
    # @allure.story('从快照创建虚拟机')
    # def test_createvm002_from_snap(self, create_vm):
    #     pass

