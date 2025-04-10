import pytest
from selenium.webdriver.common.action_chains import ActionChains
from pages_selector.find_element import FindEles
from utils.ele_action import EleAction


@pytest.fixture()
def create_vm(request):
    if not hasattr(request, 'parm'):
        raise ('无有效参数')

    page_name = 'create_vm'
    vm_create_setup_dict = request.param
    vm_create_conf = vm_create_setup_dict['vmconf']
    driver = vm_create_setup_dict['driver']
    logger = vm_create_setup_dict['logger']

    ele_find = FindEles(driver, logger)
    ele_action = EleAction(driver, ele_find, page_name, logger)

    # 部署方式
    if vm_create_conf['create_vm_method'] != '':
        ele_action.click('create_vm_method', vm_create_conf['create_vm_method'])

    # 虚拟机名称
    ele_action.input_send('vm_name_input', vm_create_conf['vm_name'])

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

    # 调度方式选择
    schedule_type = vm_create_conf['schedule_type']
    if schedule_type != '':
        ele_action.click('schedule_type_label', schedule_type)
    
    if schedule_type == '<指定主机>':
        host_ip = vm_create_conf['host_ip']
        if host_ip != '':
            ele_action.dropdown_menu_select('schedule_choice_host', 'schedule_choice_host_name', target_option_repalce=host_ip)

    # 展开更多设置
    more_setup = ele_find.find_ele(page_name, 'more_setup')
    more_setup.click()

    # 是否创建完成后自动拉起
    auto_start = vm_create_conf['auto_start']
    auto_star_checkbox = ele_find.find_ele(page_name, 'startup_setup_checkbox')
    if auto_start != auto_star_checkbox.is_selected():
        auto_star_checkbox.click()

    # 系统类型配置
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
    add_hw_button = ele_find.find_ele(page_name, 'add_hw_button')
    add_disk_button = ele_find.find_ele(page_name, 'add_hw_disk_button')
    for i in range(disk_nums):
        disk_order_name = f'vm_disk{i+1}'
        ActionChains(driver).click(add_hw_button).click(add_disk_button).perform() #添加磁盘
        if vm_create_conf[disk_order_name] != '':
            vm_disk_conf = vm_create_conf[disk_order_name]
            disk_name = f'磁盘{i+1}'
            ele_action.click('disk_conf_button', disk_name)
            disk_size = vm_disk_conf['disk_size']
            ele_action.input_send('disk_conf_input', disk_size, f'{i+1}')

    # 网卡配置
    vnic_nums = vm_create_conf['vm_nic_num']
    add_vnic_button = ele_find.find_ele(page_name, 'add_hw_vmnic_button')
    for i in range(vnic_nums):
        vnic_order_name = f'vm_nic{i+1}'
        ActionChains(driver).click(add_hw_button).click(add_vnic_button).perform() #添加网卡
        if vm_create_conf[vnic_order_name] != '':
            vnic_conf = vm_create_conf[vnic_order_name]
            vnic_name = f'网卡{i+1}'
            ele_action.click('vmnic_conf_button', vnic_name)
            #上行交换机配置
            if vnic_conf('uplink_switch_name') != '':
                ele_action.dropdown_menu_select('vmnic_conf_uplink_selector', 'vmnic_conf_uplink_select_name',
                                                selector_replace=f'{i+1}',
                                                target_option_repalce=vnic_conf('uplink_switch_name'))

            #mac地址配置
            if vnic_conf('mac_addr') != '':
                ele_action.input_send('vmnic_hwaddr_conf_input', vnic_conf('mac_addr'), f'{i+1}')

            # 防火墙配置
            if vnic_conf('firewall_name') != '':
                vnic_firewall_selector = ele_find.find_ele(page_name, 'vmnic_firewall_conf_selector', replace_str=f'{i+1}')
                vnic_firewall_selector.click()
                ele_action.dropdown_menu_select('vmnic_firewall_conf_selector', 'vmnic_firewall_conf_select_name',
                                                f'{i+1}', vnic_conf('firewall_name'))
                
            # IPv4配置
            is_use_switch = ele_find.find_ele(page_name, 'vmnic_is_use_ipv4', replace_str=f'{i+1}')
            if vnic_conf['is_use_ipv4'] == True and 'ivu-switch-checked' not in is_use_switch.get_attribute('class'):
                is_use_switch.click()
            elif vnic_conf['is_use_ipv4'] != True and 'ivu-switch-checked' in is_use_switch.get_attribute('class'):
                is_use_switch.click()
