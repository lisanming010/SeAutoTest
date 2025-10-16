from utils.ele_action import EleAction
from pages_selector.find_element import FindEles
import ipaddress
import re

class NetTools:
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger

    def dvswitch_row_text(self, dvswitch_name)-> dict:
        '''
        获取分布式交换机列表中指定行显示列的text
        默认元素为：分布式交换机ID、名称、类型、网络类型、VLAN、IPv4网段、IPv4使用情况、IPv6网段、IPv6使用情况
        上行链路、创建时间
        
        :dvswitch_name: 分布式交换机名称
        '''
        find_ele = FindEles(self.driver, self.logger)

        menu_ele_action = EleAction(self.driver, find_ele, 'page_head_index', self.logger)
        menu_ele_action.click('network_button')
        second_menu_action = EleAction(self.driver, find_ele, 'second_head_index', self.logger)
        second_menu_action.click('button', '分布式交换机')

        dv_switch_ele_action = EleAction(self.driver, find_ele, 'dvswitch', self.logger)
        dvswitch_row = dv_switch_ele_action.ele_selection('dvswitch_id', dvswitch_name, ele_kind='list').text.strip().split('\n')
        dvswitch_uplink = dvswitch_row[-2]
        dvswitch_create_time = dvswitch_row[-1]
        # 处理dvswitch_row列表，添加缺失的元素
        if dvswitch_row[5] == '-':
            dvswitch_row.insert(5, '-')
        if dvswitch_row[6] == '-':
            dvswitch_row.insert(7, '-')
        if dvswitch_row[8] == '-':
            dvswitch_row.insert(8, '-')
        
        # 其余字段无法确定相对位置，直接丢弃重新插入
        dvswitch_row = dvswitch_row[:10]

        dvswitch_row.append(dvswitch_uplink)
        dvswitch_row.append(dvswitch_create_time)

        dvswitch_row_dict = {
            'dvswitch_id': dvswitch_row[0],
            'dvswitch_name': dvswitch_row[1],
            'dvswitch_type': dvswitch_row[2],
            'dvswitch_net_type': dvswitch_row[3],
            'dvswitch_VLAN': dvswitch_row[4],
            'dvswitch_IPv4_seg': dvswitch_row[5],
            'dvswitch_IPv4_usage': dvswitch_row[6], 
            'dvswitch_IPv4_usage_rate': dvswitch_row[7], 
            'dvswitch_IPv6_seg': dvswitch_row[8],
            'dvswitch_IPv6_usage': dvswitch_row[9],
            'dvswitch_uplink': dvswitch_row[10],
            'dvswitch_create_time': dvswitch_row[11]
        }
        
        return dvswitch_row_dict
    
    @staticmethod
    def ip_handle(ip_type, ip_str)-> list:
        '''
        离散、连续IP处理，"fd02:aa1::aa1-fd02:aa1::aa3,fd02:aa1::aa8" 
                        -> ['fd02:aa1::aa1', 'fd02:aa1::aa2', 'fd02:aa1::aa3', 'fd02:aa1::aa8']

        :ip_type: IP类型：v4、 v6
        :ip_str: 需要拆解的字符串，因为校验阶段使用故不再对相关格式做校验
        '''
        ip_list = []
        ip_list_temp = ip_str.split(',')
        for i in ip_list_temp:
            if '-' not in i:
                ip_list.append(i)
            elif '-' in i:
                start_ip, end_ip = i.split('-')
                if ip_type == 'ipv6':
                    start_ip = ipaddress.IPv6Address(start_ip)
                    end_ip = ipaddress.IPv6Address(end_ip)
                if ip_type == 'ipv4':
                    start_ip = ipaddress.IPv4Address(start_ip)
                    end_ip = ipaddress.IPv4Address(end_ip)
                curr_ip = start_ip
                while curr_ip <= end_ip:
                    ip_list.append(str(curr_ip))
                    curr_ip += 1
        return ip_list
    
class OtherTools:
    def __init__(self, logger):
        self.logger = logger
        
    def mk_match_valid_string(self, title, curr_conf, des_conf, is_pass=False)-> str:
        '''
        :title: 校验类别名称
        :curr_conf: 当前实际采集到的配置信息
        :des_conf: 期望的配置信息
        :is_pass: 校验结果
        '''
        result = '失败' if is_pass == False else '通过'
        return f'{title}校验{result}，期望值为：{des_conf}, 实际值为：{curr_conf}'
    
    def replace_str_extraction(self, string)-> str:
        '''
        替换字符串提取，<replace> -> replace

        :string: 需要提取的字符串
        '''
        result = re.sub(r'[<>]', '', string)
        return result
    
    def match_vaildtion(self, vaildation_item, des_value, curr_value, use_in=False)-> bool:
        '''
        值相等校验，相等->True,不等->false

        :vaildation_item: 校验项名称
        :des_value: 期望值
        :curr_value: 实际值
        :use_in: 比较方法是否使用 in ,默认False
        '''
        assert_flag = 1
        if use_in:
            if des_value != curr_value:
                assert_flag = 0
        else:
            if des_value not in curr_value:
                assert_flag = 0

        is_pass = True if assert_flag else False
        self.logger.debug(
            self.mk_match_valid_string(vaildation_item, str(curr_value), str(des_value), is_pass=is_pass)
        )

        return assert_flag