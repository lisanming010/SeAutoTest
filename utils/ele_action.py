import selenium.common.exceptions as seEception
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from time import sleep

class EleAction():
    def __init__(self, driver, ele_find, page_name, logger):
        '''
        selenium部分动作包装类

        :driver: web driver
        :ele_find: 已完成实例化的 pages_selector.find_element.FindEles
        :page_name: 元素所处页面与element_locating中section保持一致
        '''
        self.driver = driver
        self.ele_find = ele_find.find_ele
        self.page_name = page_name
        self.logger = logger
    
    def ele_selection(self, ele_name, ele_replace=''):
        """
        元素选择器
        """
        if ele_replace == '':
            return self.ele_find(self.page_name, ele_name)
        else:
            return self.ele_find(self.page_name, ele_name, replace_target=ele_replace)


    def click(self, click_button, click_button_replace=''):
        """
        元素点击

        :click_button: 按钮元素名称，element_locating中option
        """
        if click_button_replace == '':
            button = self.ele_find(self.page_name, click_button)
        elif click_button_replace != '':
            button = self.ele_find(self.page_name, click_button, replace_target=click_button_replace)

        self.logger.info(button)
        ActionChains(self.driver).click(button).perform()
        self.logger.info(f"click: {click_button}")


    def dropdown_menu_select(self, selector, target_option, selector_replace='', target_option_repalce=''):
        """
        下拉列表选择

        :selector: 下拉列表元素名称，element_locating中option
        :target_option: 选项名称，element_locating中option
        """
        if selector_replace != '':
            self.click(selector, selector_replace)
        elif selector_replace == '':
            self.click(selector)
        sleep(0.5)

        self.driver.implicitly_wait(0) #暂时取消隐式等待
        while True: # 下拉列表分页情况处理，遍历所有页面仍未定位到元素时才抛出异常
            try:
                if target_option_repalce != '':
                    self.click(target_option, target_option_repalce)
                elif target_option_repalce == '':
                    self.click(target_option)
            except seEception.NoSuchElementException as not_fond_ele_target_option:
                try:
                    page_down_button = self.ele_find('general_common', 'select_dropdown_pagination_pgdown')
                except:
                    raise not_fond_ele_target_option
                else:
                    if 'ivu-page-disabled' in page_down_button.get_attribute('class'):
                        raise not_fond_ele_target_option
                    else:
                        page_down_button.click()
                        sleep(0.5)
            else:
                sleep(0.5)
                break
        self.driver.implicitly_wait(10)
        
    def input_send(self, input, input_content, input_ele_repalce=''):
        """
        输入框输入

        :input: 输入元素名称，element_locating中option
        :input_content: 输入内容
        """
        if input_ele_repalce == '':
            input_ele = self.ele_find(self.page_name, input)
        elif input_ele_repalce != '':
            input_ele = self.ele_find(self.page_name, input, replace_target=input_ele_repalce)

        # input_ele.clear() #部分组件无法清空，如创建虚拟机数量
        action = ActionChains(self.driver)
        action.click(input_ele).key_down(Keys.CONTROL).send_keys('a').send_keys(Keys.DELETE).key_up(Keys.CONTROL) #清空输入框原有内容
        action.send_keys(input_content)
        action.perform()
        self.logger.info(f'click: {input} and send key: {input_content}')