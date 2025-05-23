from ele_action import EleAction

class GetRowText():
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
        page_name = 'dvswitch'
        ele_action = EleAction(self.driver, page_name, self.logger)
        dvswitch_id = ele_action.ele_selection('dvswitch_id', dvswitch_name).text.strip()
        dvswitch_row = ele_action.ele_selection('dvswitch_row', dvswitch_id).text.strip().split('\n')
        dvswitch_uplink = ele_action.ele_selection('uplink_button', dvswitch_id).text.strip().split('\n')
        dvswitch_create_time = ele_action.ele_selection('create_time', dvswitch_id).text.strip().split('\n')
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