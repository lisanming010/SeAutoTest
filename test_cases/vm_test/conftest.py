import pytest
from pages_selector.find_element import FindEles
from utils.ele_action import EleAction
from time import sleep
import selenium.common.exceptions as seEception

# IP类型相关替换字段构造体
_vmnic_conf_struct = {
    'ipv4_is_use': '启用IPv4',
    'ipv6_is_use': '启用IPv6',
    'ipv4_address_input': '输入IPv4地址',
    'ipv6_address_input': '输入IPv6地址',
    'ipv4_netmask_input': 'netMask',
    'ipv6_netmask_input': 'ipv6NetMask',
    'ipv4_gateway_input': 'gatewayIp',
    'ipv6_gateway_input': 'ipv6Gateway',
    'ipv4_subip': 'IPv4子IP地址',
    'ipv6_subip': 'IPv6子IP地址'
}

def _ip_settig(vnic_conf: dict, ele_action: EleAction, vnic_order: int, logger):
    '''
    网卡IP设置IPv4、IPv6共用方法

    :ip_type: ipv4、ipv6
    :vnic_conf: 网卡配置字典
    :ele_action: 实例化完成的元素操作ele_action类
    :vnic_order: 网卡序号
    '''
    for ip_type in ['ipv4', 'ipv6']:
        replace_list = [_vmnic_conf_struct[f'{ip_type}_is_use'], vnic_order]
        try:
            is_use_switch = ele_action.ele_selection('vmnic_is_use_ip', replace_list)
        except:
            if ip_type == 'ipv6': # 系统未启用ipv6时自动忽略相关配置
                logger.warning('未找到元素：IPv6启用开关，或系统未启用IPv6开关')
                break
            else:
                raise RuntimeError('未找到元素：IPv4/IPv6启用框')
        if vnic_conf[f'is_use_{ip_type}'] == True:   
            if 'ivu-switch-checked' not in is_use_switch.get_attribute('class'):
                is_use_switch.click()

            if vnic_conf[f'{ip_type}_addr'] != '': 
                replace_list = [_vmnic_conf_struct[f'{ip_type}_address_input'], vnic_order]
                ele_action.input_send('vmnic_ip_conf_input', vnic_conf[f'{ip_type}_addr'], replace_list)

            if vnic_conf[f'{ip_type}_prefix'] != '':
                replace_list = [_vmnic_conf_struct[f'{ip_type}_netmask_input'], vnic_order]
                '''
                如果IP控件处于不可输入状态则跳过输入，如交换机选择为启用了DHCP的场景，网关字段类似
                TODO: 这种情况下assert断言也应当忽略对应判断                
                '''
                if 'ivu-input-disabled' not in ele_action.ele_selection('vmnic_ip_conf_prefix_input', replace_list).get_attribute('class'):
                    ele_action.input_send('vmnic_ip_conf_prefix_input', vnic_conf[f'{ip_type}_prefix'], replace_list)
            
            if vnic_conf[f'{ip_type}_gateway'] != '':
                replace_list = [_vmnic_conf_struct[f'{ip_type}_gateway_input'], vnic_order]
                if 'ivu-input-disabled' not in ele_action.ele_selection('vmnic_ip_conf_gateway_input', replace_list).get_attribute('class'):
                    ele_action.input_send('vmnic_ip_conf_gateway_input', vnic_conf[f'{ip_type}_gateway'], replace_list)

            # 子IP配置
            subip_type = _vmnic_conf_struct[f'{ip_type}_subip'] 
            if vnic_conf[f'{ip_type}_subip_is_use']:
                replace_list = [subip_type, vnic_order]
                ele_action.click('vmnic_subip_checkbox', replace_list)

                if vnic_conf[f'{ip_type}_subip_set_mode'] == '随机':
                    replace_list = [subip_type, vnic_order]
                    ele_action.input_send('vmnic_subip_nums_input', vnic_conf[f'{ip_type}_subip_random_nums'], replace_list)
                if vnic_conf[f'{ip_type}_subip_set_mode'] == '指定':
                    replace_list = [subip_type, vnic_order]
                    try:
                        ele_action.click('vmnic_subip_appoint_radio', replace_list)
                    except seEception.TimeoutException:
                        # 连接到不启用DHCP的交换机时选择启用子IP时无IP方式设置
                        pass
                    ele_action.input_send('vmnic_subip_appoint_input', vnic_conf[f'{ip_type}_subip_appoint_addr'], replace_list)
                    # sleep(10)
        elif vnic_conf[f'is_use_{ip_type}'] == False and 'ivu-switch-checked' in is_use_switch.get_attribute('class'):
            is_use_switch.click()

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
    sleep(1)

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
        ele_action.dropdown_menu_select('group_selector', 'group_select_name', 
                                        target_option_repalce=group_name)

    # 存储池选择
    storage_name = vm_create_conf['storage_pool_name']
    if storage_name != '':
        ele_action.dropdown_menu_select('storage_selector', 'storage_select_name', 
                                        target_option_repalce=storage_name)
        ele_action.click('vm_name_input', vm_create_conf['vm_name'])

    sleep(1)
    # 调度方式选择
    schedule_type = vm_create_conf['schedule_type']
    if schedule_type != '':
        ele_action.click('schedule_type_label', schedule_type)
    if schedule_type == '<指定主机>':
        host_ip = vm_create_conf['host_ip']
        if host_ip != '':
            ele_action.dropdown_menu_select('schedule_choice_host', 'schedule_choice_host_name', 
                                            target_option_repalce=host_ip)

    ele_action.click('vm_name_input')

    # 展开更多设置
    ele_action.click('more_setup')
    # 是否创建完成后自动拉起
    auto_start = vm_create_conf['auto_start']
    auto_star_checkbox = ele_find.find_ele(page_name, 'startup_setup_checkbox')
    if auto_start != auto_star_checkbox.is_selected():
        auto_star_checkbox.click()

    # 系统类型配置,非全新创建虚拟机时跳过改选项设置
    if vm_create_conf['create_vm_method'] == '<全新虚拟机>':
        system_type = vm_create_conf['system_type']
        if system_type != '':
            ele_action.click('system_type', system_type)

    # 引导类型
    if vm_create_conf['create_vm_method'] == '<全新虚拟机>':
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
        ele_action.dropdown_menu_select('cpu_conf_socket_num_selector', 'cpu_conf_socket_num', 
                                        target_option_repalce=cpu_soket_num)
    
    # cpu绑核设置
    is_bind_core = vm_create_conf['is_bind_core']
    if is_bind_core:
        core_map = vm_create_conf['core_map']
        cpu_bind_core_switch = ele_action.ele_selection('cpu_bind_core_switch')
        cpu_bind_core_switch_class = cpu_bind_core_switch.get_attribute('class')
        if 'ivu-switch-checked' in cpu_bind_core_switch_class or 'ivu-switch-disabled' in cpu_bind_core_switch_class:
            pass
        else:
            # cpu绑核控件点击
            cpu_bind_core_switch.click()
            ele_action.click('cpu_bind_core_setting')

            # 遍历核心，每个核心执行绑核
            for core_num in range(int(cpu_core_num)):
                vcpu_map = core_map.get(str(core_num), None)
                if vcpu_map == None:
                    continue
                
                # 点击pcpu选择控件
                pcpu_select_button = ele_action.ele_selection('pcpu_select_button', str(core_num + 1)) 
                pcpu_select_button.click()
                sleep(0.5)
                # cpu绑核map解析
                for numa, cores in vcpu_map.items():
                    numa_index = numa.split(' ')[-1]
                    for core_index in cores:
                        # 前端元素缺少是否展开标志位，所以第一次未捕获到check_box时尝试点击列表展开，展开后仍为捕获到则抛出异常
                        for loop_time in range(1):
                            try:
                                numa_core_check_box = ele_action.ele_selection('numa_core_check_box', ele_replace=[numa_index, str(core_index)], find_list=True)
                                numa_core_check_box[-1].click()
                            except seEception.NoSuchElementException as e:
                                if loop_time == 0:
                                    ele_action.click('numa_core_check_box_expand', numa_index)
                                    sleep(0.5)
                                else:
                                    raise e
                pcpu_select_button.click()
            ele_action.click('cpu_bind_core_setting_close')
            sleep(0.5)

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
            for i in range(vnic_nums - 1):
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
                                                    target_option_repalce=[vnic_conf['uplink_switch_name'], vnic_order],
                                                    pgdown_replace=vnic_order)
                
                #mac地址配置
                if vnic_conf['mac_addr'] != '':
                    ele_action.input_send('vmnic_hwaddr_conf_input', vnic_conf['mac_addr'], vnic_order)

                # 防火墙配置
                if vnic_conf['firewall_name'] != '':
                    ele_action.dropdown_menu_select('vmnic_firewall_conf_selector', 'vmnic_firewall_conf_select_name',
                                                    vnic_order, vnic_conf['firewall_name'])
                # ip设置
                _ip_settig(vnic_conf, ele_action, vnic_order, logger)

                #展开网卡高级设置
                ele_action.click('vmnic_conf_advanced', vnic_order)

                #网卡上下线配置
                if vnic_conf['is_online'] == False:
                    ele_action.click('vmnic_conf_offline_radio', vnic_order)
                
                #ip地址检查配置
                ele_ipcheck_checkbox = ele_action.ele_selection('vmnic_conf_ipcheck_checkbox', vnic_order)
                is_checked = ele_ipcheck_checkbox.get_attribute('class')
                if vnic_conf['is_ipcheck'] == False:
                    if 'ivu-checkbox-wrapper-checked' in is_checked:
                        ele_ipcheck_checkbox.click()
                elif vnic_conf['is_ipcheck'] == True:
                    if 'ivu-checkbox-wrapper-checked' not in is_checked:
                        ele_ipcheck_checkbox.click()

                #出入站带宽限制
                if vnic_conf['in_bandwidth'] != '':
                    ele_action.click('vmnic_conf_in_bandwidth_checkbox', vnic_order)
                    # ele_action.click('vmnic_conf_in_bandwidth_checkbox')
                    # vnic_bandwidth_checkbox = ele_action.ele_selection('vmnic_conf_in_bandwidth_checkbox', vnic_order)
                    # vnic_bandwidth_checkbox.click()
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
                if iso_conf['is_external_iso'] == False:
                    replace_list = [iso_conf['associated_storage_pool'], iso_conf['iso_name_or_link']]
                    ele_action.dropdown_menu_select('optical_driver_selector', 'optical_driver_select_name',
                                                    iso_order, replace_list, ele_kind='popup')
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
    
    return driver, logger, vm_create_conf
