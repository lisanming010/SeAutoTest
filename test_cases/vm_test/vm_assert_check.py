from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from pages_selector.find_element import FindEles
from utils.ele_action import EleAction
from time import sleep
from utils.tools import Tools
import selenium.common.exceptions as seEception

class AssertCheck():
    def __init__(self, driver, logger, vm_conf: dict):
        '''
        虚拟机相关断言判定

        :driver: webdriver
        :logger: 实例化完成的logger类
        :vm_conf: 虚拟机创建配置，dict
        '''
        self.driver = driver
        self.logger = logger
        self.vm_conf = vm_conf
        
        ele_find = FindEles(self.driver, self.logger)
        self.vm_list_selector = EleAction(self.driver, ele_find, 'vm_list', self.logger)
        self.vmconf_details_selector = EleAction(self.driver, ele_find, 'vm_hw_conf_details', self.logger)
        self.general_common = EleAction(self.driver, ele_find, 'general_common', self.logger)

    def vm_list_get_allIp(self, vm_id)-> dict:
        '''
        获取虚拟机列表中虚拟机所有IP

        :vm_id: 虚拟机ID
        -> dict{'IPv4':[], 'IPv6':[]}
        '''

        ip_dict = {
            'IPv4': [],
            'IPv6': []
        }
        try:
            ip_expan_button = self.vm_list_selector.ele_selection('vm_ip_address_expan')
        
        except seEception.NoSuchElementException:
            # 未定位到展开按钮时默认判定为单个IP，可能存在定位异常时误判
            ip_addr_text = self.vm_list_selector.ele_selection('vm_ip_address', vm_id).text.strip()
            if '.' in ip_addr_text:
                ip_dict['IPv4'].append(ip_addr_text)
            elif ':' in ip_addr_text:
                ip_dict['IPv6'].append(ip_addr_text)
            return ip_dict
        
        else:
            # 多IP展开逻辑分支
            ActionChains(self.driver).move_to_element(ip_expan_button).perform()
            ip_expan_text = self.vm_list_selector.ele_selection('vm_ip_address_expan_text').text.strip().split('\n')
            if '更多' in ip_expan_text:
                ip_more_button = self.vm_list_selector.ele_selection('vm_ip_address_expan_more')
                ActionChains(self.driver).move_to_element(ip_more_button).click(ip_more_button).perform()
                pgdown_button = self.general_common.ele_selection('popup_list_pgdown')
                ip_list_temp = []
                while True:
                    ip_list_temp.extend(self.vm_list_selector.ele_selection('vm_ip_list').text.strip().split())
                    if 'ivu-page-disabled' not in pgdown_button.get_attribute('class'):
                        break
                    else:
                        pgdown_button.click()
                # 列表处理       
                for i in ip_list_temp:
                    if '.' in i:
                        ip_dict['IPv4'].append(i)
                    elif ':' in i:
                        ip_dict['IPv6'].append(i)
            else:
                key = 'IPv4'
                for i in ip_expan_text:
                    if 'IPv4' in i:
                        key = 'IPv4'
                        continue
                    elif 'IPv6' in i:
                        key = 'IPv6'
                        continue
                    ip_dict[key].append(i)
            return ip_dict

    def vm_list_state_check(self, vm_id, desired_state)-> bool:
        '''
        虚拟机状态校验

        :vm_id: 虚拟机ID
        :desired_state: 期望状态
        -> assert_flag int(0,1)
        '''
        assert_flag = 1
        loop_time = 100
        while True:
            sleep(3)
            vm_curr_state = self.vm_list_selector.ele_selection('vm_stat', vm_id).text.strip()
            if desired_state in vm_curr_state:
                break
            elif loop_time == 0:
                self.logger.error(f'虚拟机{vm_id}当前状态与预期状态不一致，当前状态:{vm_curr_state},预期状态:{desired_state},dl:{loop_time*3}s')
                assert_flag = 0
                break
            else:
                loop_time -= 1
        return assert_flag                    

    def vm_list_ip_check(self, vm_id, vnic_conf:dict):
        assert_flag = 1

        is_use_ipv4 = vnic_conf['is_use_ipv4']
        ipv4_addr = vnic_conf['ipv4_addr']
        is_use_ipv6 = vnic_conf['is_use_ipv6']
        ipv6_addr = vnic_conf['ipv6_addr']

        ip_dict = self.vm_list_get_allIp(vm_id)
        uplink_switch_name = vnic_conf['uplink_switch_name']
        dvswith_info_dict = Tools.dvswitch_row_text(uplink_switch_name)
        # 连接到启用DHCP的交换机，仅校验是否获取IP
        if dvswith_info_dict['dvswitch_IPv4_seg'] != '-':
            #连接到启用了DHCP的交换机
            pass
        elif dvswith_info_dict['dvswitch_IPv4_seg'] == '-':
            #连接到不启用DHCP的交换机
            ipv4_list = []
            if is_use_ipv4:
                ipv4_main_ip = vnic_conf['ipv4_addr']
                ipv4_list.append(ipv4_main_ip)
                if vnic_conf['ipv4_subip_is_use']:
                    if vnic_conf['ipv4_subip_set_mode'] == '指定':
                        sub_ip_list = Tools.ip_handle('ipv4', vnic_conf['ipv4_subip_appoint_addr'])
                        ipv4_list.extend(sub_ip_list)
                    elif vnic_conf['ipv4_subip_set_mode'] == '随机':
                        for i in range(vnic_conf['ipv4_subip_random_nums']):
                            ipv4_list.append(f'random_ip_placeholder{i}')
            if is_use_ipv6:
                pass
      
    def vm_list_scale_check(self):
        pass

    def vm_list_host_check(self):
        pass

    def vm_create_hw_conf_check(self):
        assert_flag = 1
        
        vm_create_num = self.vm_conf['vm_create_num']
        vm_name_pre = self.vm_conf['vm_name']
        vm_distribution = {}
        #批量创建依次校验
        for i in range(vm_create_num):
            if vm_create_num == 1:
                vm_name = vm_name_pre
            else:
                vm_name = f'{vm_name_pre}-{i + 1}'
            try:
                vm_name_button = self.vm_list_selector.ele_selection('vm_name_button', vm_name, ele_kind='list')
            except seEception.NoSuchElementException:
                # 查找不到虚拟机记录，判断为创建失败。
                # TODO：添加日志采集输出错误详情，看是用se还是走接口
                assert_flag = 0
                self.logger.error(f'虚拟机{vm_name}创建失败或找不到虚拟机记录')
                return assert_flag
            else:
                '''运行状态判断'''
                vm_id_ele = self.vm_list_selector.ele_selection('vm_id', vm_name)
                #输出对应虚拟机整列text，ID、名称、状态、规模、主机IP、创建人
                vm_line_text = vm_id_ele.text.strip().split('\n')
                vm_id = vm_line_text[0]
                if self.vm_conf['auto_start']:
                    vm_desired_state = '运行中'
                else:
                    vm_desired_state = '已关机'
                assert_flag = self.vm_list_state_check(vm_id, vm_desired_state)
                if not assert_flag:
                    return assert_flag
                
                '''虚拟机网卡相关配置校验'''
                vm_list_ips = self.vm_list_get_allIp(vm_id)
                curr_vnic_num = 0
                vm_name_button.click()
                sleep(2)
                vnic_num = self.vm_conf['vm_nic_num']
                try:
                    vnic_selector = self.vmconf_details_selector.ele_selection('vnics', find_list=True)
                    curr_vnic_num = len(vnic_selector)
                except seEception.NoSuchElementException:
                    # 不添加网卡时落入该分支
                    pass

                if curr_vnic_num != vnic_num:
                    self.logger.error(f"虚拟机实际网卡数量与配置期望数量不符，期望数量：{vnic_num}, 实际数量：{curr_vnic_num}")
                    return 0
                elif curr_vnic_num == vnic_num == 0:
                    self.logger.debug('虚拟机网卡相关配置校验通过！虚拟机未绑定网卡')
                elif curr_vnic_num == vnic_num:
                    for i in range(vnic_num):
                        vnic_order = f'{i+1}'
                        vnic_name = f'vm_nic{vnic_order}'
                        vnic_conf = self.vm_conf[vnic_name]

                        vnic_curr_overview_button = self.vmconf_details_selector.ele_selection('vnic_overview', ele_replace=vnic_order)
                        # 输出网卡概览：IP(mac：不启用DHCP的交换机)|交换机名称|防火墙
                        vnic_curr_overview_text = vnic_curr_overview_button.text.strip()
                        vnic_curr_overview_list = vnic_curr_overview_text.split('|')

                        '''上行交换机验证'''
                        # 网卡侧
                        if vnic_curr_overview_list[1].strip() not in vnic_conf['uplink_switch_name']:
                            self.logger.error(f"网卡校验失败，网卡上行交换机与预期不符，预期上行{vnic_conf['uplink_switch_name']}，\
                                              实际上行{vnic_curr_overview_list[1]}")
                            return 0
                        vnic_curr_overview_button.click()
                        sleep(0.5)
                        vnic_detail = self.vmconf_details_selector.ele_selection('vnic_detail', ele_replace=vnic_order, find_list=True)
                        nic_detail_dict = {}
                        for i in vnic_detail:
                            key, value = i.text.split('\n')
                            if '管理子IP' in value:
                                value, _ = value.split(' ')
                            nic_detail_dict[key] = value
                        self.logger.debug(nic_detail_dict)

                        '''IP地址验证'''


                        '''MAC配置检查'''
                        mac = vnic_conf['mac_addr']
            
                '''所属节点判断'''
                vm_host = vm_line_text[4]
                if self.vm_conf['schedule_type'] == '<指定主机>':
                    if vm_host not in self.vm_conf['host_ip']:
                        assert_flag = 0
                        self.logger.error(f"虚拟机{vm_name}所属主机位置有误，指定节点：\
                                          {self.vm_conf['schedule_type']}，实际运行节点：{vm_host}")
                else: 
                    #TODO: 批量批量创建验证调度
                    # 统计本次批量创建虚拟机所属物理节点分布，{'node_ip': times,...}
                    if vm_host not in vm_distribution:
                        vm_distribution[f'{vm_host}'] = 1
                    else:
                        vm_distribution[f'{vm_host}'] += 1

        return assert_flag
    