import selenium.common.exceptions as seEception
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from time import sleep
from typing import TYPE_CHECKING

class EleAction:
    def __init__(self, driver, ele_find, page_name: str, logger):
        '''
        selenium部分动作包装类

        :driver: web driver
        :ele_find: 已完成实例化的 pages_selector.find_element.FindEles
        :page_name: 元素所处页面与element_locating中section保持一致
        '''
        self.driver = driver
        self._ele_find = ele_find.find_ele
        self._ele_find_base_ele = ele_find.find_ele_base_ele
        self.page_name = page_name
        self.logger = logger

    def ele_selection_base_ele(self, ele, by, follow_path, find_list=False):
        '''
        追加定位，支持基于已有元素扩展定位，对ele.find_element()封装

        :ele: webelement对象
        :by: 定位方式，目前仅支持xpath
        :follow_path: 相对ele对象的路径
        :find_list: 是否调用find_elements,默认为false
        ->webelement(s)
        '''
        return self._ele_find_base_ele(ele, by, follow_path, find_list)

    def ele_selection(self, ele_name: str, ele_replace='', page_local='', ele_kind = '',
                      pgdown_selction='', pgdown_replace='', find_list=False):
        """
        元素选择器

        :ele_name: 元素定位文件option中元素名称
        :page_local: 元素定位文件selector名称，不指定时使用类初始化时指定位置
        :ele_replace: 元素名称中替换文本
        :find_list: 是否使用find_elements
        --> ele(s)
        """
        page_name = self.page_name
        if page_local != '':
            page_name = page_local

        pgdown_selction = 'list_pgdown' if pgdown_selction == '' else pgdown_selction
 
        if ele_kind == '':
            if ele_replace == '':
                return self._ele_find(page_name, ele_name, find_list=find_list)
            else:
                return self._ele_find(page_name, ele_name, replace_target=ele_replace, find_list=find_list)


        #分页控件便利页面查询
        self.driver.implicitly_wait(1)
        while True:
            try:
                if ele_replace == '':
                    ele = self._ele_find(page_name, ele_name, find_list=find_list)
                else:
                    ele = self._ele_find(page_name, ele_name, replace_target=ele_replace, find_list=find_list)
            except seEception.NoSuchElementException as not_fond_ele_target_option: #未找到元素时进入翻页遍历逻辑
                try:
                    if ele_kind == 'list':
                        page_down_button = self._ele_find(page_name, pgdown_selction) #判断是否有分页控件
                    elif ele_kind == 'selector':
                        page_down_button = self._ele_find('general_common', 'select_dropdown_pagination_pgdown', replace_target=pgdown_replace)
                    elif ele_kind == 'popup':
                        page_down_button = self._ele_find('general_common', 'popup_list_pgdown', )
                except Exception as e:
                    self.driver.implicitly_wait(10)
                    self.logger.error(f'except error:{e}')
                    raise not_fond_ele_target_option
                else:
                    if 'ivu-page-disabled' in page_down_button.get_attribute('class'): #判断是否为最后一页
                        self.driver.implicitly_wait(10)
                        self.logger.debug(f'已到最后一页')
                        raise not_fond_ele_target_option
                    else:
                        self.driver.implicitly_wait(3)
                        page_down_button.click()
                        sleep(0.5)
            else:
                self.driver.implicitly_wait(10)
                return ele


    def click(self, click_button, click_button_replace='', ele_kind = ''):
        """
        元素点击

        :click_button: 按钮元素名称，element_locating中option
        """
        if click_button_replace == '':
            button = self.ele_selection(click_button, ele_kind=ele_kind)
        elif click_button_replace != '':
            button = self.ele_selection(click_button, click_button_replace, ele_kind=ele_kind)

        self.logger.info(button)
        ActionChains(self.driver).click(button).perform()
        self.logger.info(f"click: {click_button}")


    def dropdown_menu_select(self, selector, target_option, selector_replace='', 
                            target_option_repalce='', pgdown_replace='', 
                            ele_kind='selector', sleep_time=1):
        """
        下拉列表选择

        :selector: 下拉列表元素名称，element_locating中option
        :target_option: 选项名称，element_locating中option
        :ele_kind: 元素选择类型，可选 selector、popup
        """
        selector_button = self.ele_selection(selector, selector_replace)
        selector_button.click()
        sleep(sleep_time)

        target_button = self.ele_selection(target_option, target_option_repalce, pgdown_replace=pgdown_replace, ele_kind=ele_kind)
        target_button.click()
        
        
    def input_send(self, input, input_content, input_ele_repalce=''):
        """
        输入框输入

        :input: 输入元素名称，element_locating中option
        :input_content: 输入内容
        """
        if input_ele_repalce == '':
            input_ele = self._ele_find(self.page_name, input)
        elif input_ele_repalce != '':
            input_ele = self._ele_find(self.page_name, input, replace_target=input_ele_repalce)

        # input_ele.clear() #部分组件无法清空，如创建虚拟机数量
        action = ActionChains(self.driver)
        action.click(input_ele).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).send_keys(Keys.DELETE) #清空输入框原有内容
        action.send_keys(input_content)
        action.perform()
        self.logger.info(f'click: {input} and send key: {input_content}')

    def get_list_td_text(self, tbody_path:str, table_pgdown:str, tbody_path_replace='', pgdown_replace='', drop_empty=True)->list:
        '''
        获取列表中全部td的text值，返回列表，调用时需要tbody可定位

        :tbody: 列表tbody定位路径，当前仅支持xpath
        :table_pgdown: 列表“下一页”按钮定位路径
        :tbody_path_replace: 
        :drop_empty: 是否丢弃空白记录
        ->[tr[td,td],]
        '''

        tbody_ele = self.ele_selection(tbody_path, tbody_path_replace)
        pgdown_ele = self.ele_selection(table_pgdown, pgdown_replace)
        td_list = []
        while True:
            sleep(0.5)
            tr_eles = self.ele_selection_base_ele(tbody_ele, 'xpath', './/tr', find_list=True)
            for tr_ele in tr_eles:
                td_eles = self.ele_selection_base_ele(tr_ele, 'xpath', './/td', find_list=True)
                td_tmp = []
                for td_ele in td_eles:
                    if td_ele.text == '' and drop_empty:
                        continue
                    td_tmp.append(td_ele.text)
                td_list.append(td_tmp)
            
            if 'ivu-page-disabled' in pgdown_ele.get_attribute('class'):
                break
            else:
                pgdown_ele.click()
        
        return td_list
