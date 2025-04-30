import pytest
from selenium.webdriver.common.action_chains import ActionChains
from pages_selector.find_element import FindEles
from utils.ele_action import EleAction
from time import sleep


@pytest.fixture(scope='function')
def create_vm(request, login_driver):
    driver, logger = login_driver
    if not hasattr(request, 'param'):
        raise TypeError('无有效参数')

    page_name = 'create_vm'
    vm_create_setup_dict = request.param
    vm_create_conf = vm_create_setup_dict['vmconf']

    ele_find = FindEles(driver, logger)
    ele_action = EleAction(driver, ele_find, page_name, logger)

    ele_find.find_ele('page_head_index', 'compute_button').click()
    ele_find.find_ele('computer_list_head', 'create_vm_button').click()

    # 部署方式
    if vm_create_conf['create_vm_method'] != '':
        ele_action.click('create_vm_method', vm_create_conf['create_vm_method'])

    # 虚拟机名称
    ele_action.input_send('vm_name_input', vm_create_conf['vm_name'])

    # 模板选择，部署方式选择非模板部署时自动跳过相关选项
    if vm_create_conf['create_vm_method'] == '<从模板部署>':
        if vm_create_conf['vm_temp_id'] and vm_create_conf['vm_temp_name'] != '':
            temp_select_replace_list = [vm_create_conf['vm_temp_id'], vm_create_conf['vm_temp_name']]
            ele_action.dropdown_menu_select('temp_selector', 'temp_select_name', 
                                            target_option_repalce=temp_select_replace_list)

    # 集群选择
    vcluster_select_label = vm_create_conf['vcluster']
    if vcluster_select_label != '':
        ele_action.click('vcluster_select_label', vm_create_conf['vcluster'])

    # 分组选择
    group_name = vm_create_conf['group_name']
    if group_name != '':
        ele_action.dropdown_menu_select('group_selector', 'group_select_name', target_option_repalce=group_name)

    # 存储池选择
    storage_name = vm_create_conf['storage_pool_name']
    if storage_name != '':
        ele_action.dropdown_menu_select('storage_selector', 'storage_select_name', target_option_repalce=storage_name)
        ele_action.click('vm_name_input', vm_create_conf['vm_name'])

    sleep(3)
    # 调度方式选择
    schedule_type = vm_create_conf['schedule_type']
    if schedule_type != '':
        ele_action.click('schedule_type_label', schedule_type)
    if schedule_type == '<指定主机>':
        host_ip = vm_create_conf['host_ip']
        if host_ip != '':
            ele_action.dropdown_menu_select('schedule_choice_host', 'schedule_choice_host_name', target_option_repalce=host_ip)

    ele_action.click('vm_name_input')

    # 展开更多设置
    ele_action.click('more_setup')

    # 是否创建完成后自动拉起
    auto_start = vm_create_conf['auto_start']
    auto_star_checkbox = ele_find.find_ele(page_name, 'startup_setup_checkbox')
    if auto_start != auto_star_checkbox.is_selected():
        auto_star_checkbox.click()

    # 系统类型配置,非全新创建虚拟机时跳过改选项设置
    if vm_create_conf['create_vm_method'] != '<全新虚拟机>':
        system_type = vm_create_conf['system_type']
        if system_type != '':
            ele_action.click('system_type', system_type)

    # 引导类型
    boot_type = vm_create_conf['boot_type']
    if boot_type != '':
        ele_action.click('boot_type', boot_type)

    # 备注
    if vm_create_conf['remark'] != '':
        ele_action.input_send('remark_input', vm_create_conf['remark'])

    # cpu配置
    cpu_core_num = vm_create_conf['cpu_core_num']
    cpu_soket_num = vm_create_conf['cpu_socket_num']
    ele_action.click('cpu_conf_button')
    ele_action.input_send('cpu_conf_input', cpu_core_num)
    if cpu_soket_num != '':
        ele_action.click('cpu_conf_advanced')
        ele_action.dropdown_menu_select('cpu_conf_socket_num_selector', 'cpu_conf_socket_num', target_option_repalce=cpu_soket_num)

    # 内存配置
    memory_size = vm_create_conf['memory_size']
    if memory_size != '':
        ele_action.click('memory_conf_button')
        ele_action.input_send('memory_conf_input', memory_size)
    
    # 磁盘配置
    disk_nums = vm_create_conf['vm_disk_num']
    if disk_nums > 0:
        if disk_nums > 1:
            for _ in range(disk_nums):
                ele_action.click('add_hw_button')
                ele_action.click('add_hw_disk_button')
        for i in range(disk_nums):
            disk_order_name = f'vm_disk{i+1}'
            if vm_create_conf[disk_order_name] != '':
                vm_disk_conf = vm_create_conf[disk_order_name]
                disk_name = f'磁盘{i+1}'
                ele_action.click('disk_conf_button', disk_name)
                disk_size = vm_disk_conf['disk_size']
                ele_action.input_send('disk_conf_input', disk_size, f'{i+1}')
    elif disk_nums == 0:
        ele_action.click('disk_conf_reduce_button', '磁盘1')

    # 网卡配置
    vnic_nums = vm_create_conf['vm_nic_num']
    if vnic_nums > 0:
        if vnic_nums > 1:
            for i in range(vnic_nums):
                ele_action.click('add_hw_button')
                ele_action.click('add_hw_vmnic_button')
        for i in range(vnic_nums):
            vnic_order_name = f'vm_nic{i+1}'
            vnic_order = f'{i+1}'
            if vm_create_conf[vnic_order_name] != '':
                vnic_conf = vm_create_conf[vnic_order_name]
                vnic_name = f'网卡{i+1}'
                ele_action.click('vmnic_conf_button', vnic_name)
                #上行交换机配置
                if vnic_conf['uplink_switch_name'] != '':
                    ele_action.dropdown_menu_select('vmnic_conf_uplink_selector', 'vmnic_conf_uplink_select_name',
                                                    selector_replace=vnic_order,
                                                    target_option_repalce=vnic_conf['uplink_switch_name'])
                
                #mac地址配置
                if vnic_conf['mac_addr'] != '':
                    ele_action.input_send('vmnic_hwaddr_conf_input', vnic_conf['mac_addr'], vnic_order)

                # 防火墙配置
                if vnic_conf['firewall_name'] != '':
                    ele_action.dropdown_menu_select('vmnic_firewall_conf_selector', 'vmnic_firewall_conf_select_name',
                                                    vnic_order, vnic_conf['firewall_name'])
                    
                # IPv4配置
                is_use_switch = ele_find.find_ele(page_name, 'vmnic_is_use_ipv4', replace_target=f'{i+1}')
                if vnic_conf['is_use_ipv4'] == True:
                    if 'ivu-switch-checked' not in is_use_switch.get_attribute('class'):
                        is_use_switch.click()
                    if vnic_conf['ipv4_addr'] != '':
                        ele_action.input_send('vmnic_ipv4_conf_input', vnic_conf['ipv4_addr'], vnic_order)
                    if vnic_conf['ipv4_prefix'] != '':
                        ele_action.input_send('vmnic_ipv4_conf_prefix_input', vnic_conf['ipv4_prefix'], vnic_order)
                    if vnic_conf['ipv4_gateway'] != '':
                        ele_action.input_send('vmnic_ipv4_conf_gateway_input', vnic_conf['ipv4_gateway'], vnic_order)
                elif vnic_conf['is_use_ipv4'] == False and 'ivu-switch-checked' in is_use_switch.get_attribute('class'):
                    is_use_switch.click()

                #展开网卡高级设置
                ele_action.click('vmnic_conf_advanced', vnic_order)

                #网卡上下线配置
                if vnic_conf['is_online'] == False:
                    ele_action.click('vmnic_conf_offline_radio', vnic_order)
                
                #ip地址检查配置
                if vnic_conf['is_ipcheck'] == False:
                    ele_action.click('vmnic_conf_ipcheck_checkbox', vnic_order)

                #出入站带宽限制
                if vnic_conf['in_bandwidth'] != '':
                    ele_action.click('vmnic_conf_in_bandwidth_checkbox', vnic_order)
                    ele_action.input_send('vmnic_conf_in_bandwidth_input', vnic_conf['in_bandwidth'], vnic_order)
                if vnic_conf['out_bandwidth'] != '':
                    ele_action.click('vmnic_conf_out_bandwidth_checkbox', vnic_order)
                    ele_action.input_send('vmnic_conf_out_bandwidth_input', vnic_conf['out_bandwidth'], vnic_order)

                #网卡多队列设置
                if vnic_conf['vnic_queue'] != '':
                    ele_action.click('vmnic_conf_queues_checkbox', vnic_order)
                    ele_action.dropdown_menu_select('vmnic_conf_queues_selector', 'vmnic_conf_queues_select_name',
                                                    vnic_order, vnic_conf['vnic_queue'])
    if vnic_nums == 0:
        ele_action.click('vmnic_reduce_button', '网卡1')
    
    #光驱配置
    iso_num = vm_create_conf['iso_num']
    if iso_num > 0:
        for i in range(iso_num):
            iso_order = f'{i+1}'
            iso_oder_name = f'光驱{i+1}'
            iso_conf = vm_create_conf[f'iso{iso_order}']
            ele_action.click('optical_driver_button', iso_oder_name)
            if iso_conf != '':
                if iso_conf['is_external_iso'] is False:
                    replace_list = [iso_conf['associated_storage_pool'], iso_conf['iso_name_or_link']]
                    ele_action.dropdown_menu_select('optical_driver_selector', 'optical_driver_select_name',
                                                    iso_order, replace_list)
                else:
                    ele_action.input_send('optical_driver_input', iso_conf['iso_name_or_link'], iso_order)
                ele_action.click('optical_driver_submit', iso_order)
    
    #usb配置
    sleep(1)
    usb_num = vm_create_conf['usb_num']
    if usb_num > 0:
        for i in range(usb_num):
            usb_order = f'{i+1}'
            usb_order_name = f'USB{i+1}'
            ele_action.click('add_hw_button')
            ele_action.click('add_hw_usb_button')
            usb_conf = vm_create_conf[f'usb{usb_order}']
            ele_action.click('usb_conf_button', usb_order_name)
            if usb_conf != '':
                ele_action.dropdown_menu_select('usb_conf_selector', 'usb_conf_select_name',
                                                usb_order, usb_conf['usb_id'])
    
    #创建数量设置
    if vm_create_conf['vm_create_num'] != 0:
        ele_action.input_send('vm_conf_summarize_create_nums_input', vm_create_conf['vm_create_num'])

    ele_action.click('vm_create_button')
    sleep(5)
    
    return driver, logger

@pytest.fixture()
def vm_hw_conf_check():
    pass