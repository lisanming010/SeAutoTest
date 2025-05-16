from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from pages_selector.find_element import FindEles
from utils.ele_action import EleAction
from time import sleep
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
        self.vmconf_details_page_selector = EleAction(self.driver, ele_find, 'vm_hw_conf_details', self.logger)

    def vm_create_hw_conf_check(self):
        assert_flag = 1
        
        vm_create_num = self.vm_conf['vm_create_num']
        vm_name_pre = self.vm_conf['vm_name']
        vm_distribution = {}
        for i in range(vm_create_num): #批量创建依次校验
            if vm_create_num == 1:
                vm_name = vm_name_pre
            else:
                vm_name = f'{vm_name_pre}-{i + 1}'
            try:
                vm_name_button = self.vm_list_selector.ele_selection('vm_name_button', vm_name, ele_kind='list')
            except seEception.NoSuchElementException: # 查找不到虚拟机记录，判断为创建失败。TODO：添加日志采集输出错误详情，看是用se还是走接口
                assert_flag = 0
                self.logger.error(f'虚拟机{vm_name}创建失败或找不到虚拟机记录')
            else:
                '''运行状态判断'''
                vm_id_ele = self.vm_list_selector.ele_selection('vm_id', vm_name)
                vm_line_text = vm_id_ele.text.strip().split('\n') #输出对应虚拟机整列text，ID、名称、状态、规模、主机IP、创建人
                vm_id = vm_line_text[0]
                while True:
                    sleep(3)
                    vm_statu = self.vm_list_selector.ele_selection('vm_stat', vm_id).text.strip()
                    if self.vm_conf['auto_start']:
                        if '已关机' in vm_statu:
                            assert_flag = 0
                            self.logger.error(f'虚拟机{vm_name}运行状态有误，创建要求：开机，实际状态为：关机')
                        elif '运行中' in vm_statu:
                            break
                    else:
                        if '已关机' in vm_statu:
                            break
                
                '''虚拟机IP设置判断'''
                if self.vm_conf['c'] != '':
                    vm_ip_address_ele = self.vm_list_selector.ele_selection('vm_ip_address', vm_id)
                    vm_ip_address = vm_ip_address_ele.text.strip()
                    if vm_ip_address != self.vm_conf['ipv4_addr']:
                        assert_flag = 0
                        self.logger.error(f'虚拟机{vm_name}IP错误，指定IP为：{self.vm_conf["vm_conf"]},实际虚拟机IP为：{vm_ip_address}')
                
                '''所属节点判断'''
                vm_host = vm_line_text[4]
                if self.vm_conf['schedule_type'] == '<指定主机>':
                    if vm_host not in self.vm_conf['host_ip']:
                        assert_flag = 0
                        self.logger.error(f"虚拟机{vm_name}所属主机位置有误，指定节点：{self.vm_conf['schedule_type']}，实际运行节点：{vm_host}")
                else: #TODO: 批量批量创建验证调度
                    if vm_host not in vm_distribution: # 统计本次批量创建虚拟机所属物理节点分布，{'node_ip': times,...}
                        vm_distribution[f'{vm_host}'] = 1
                    else:
                        vm_distribution[f'{vm_host}'] += 1

        return assert_flag
    