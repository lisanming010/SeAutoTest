from selenium.webdriver.common.action_chains import ActionChains
class EleAction():
    def __init__(self, driver, ele_find, page_name):
        '''
        selenium部分动作包装类

        :driver: web driver
        :ele_find: 已完成实例化的 pages_selector.find_element.FindEles
        :page_name: 元素所处页面与element_locating中section保持一致
        '''
        self.driver = driver
        self.ele_find = ele_find.find_ele
        self.page_name = page_name
    
    def click(self, click_button, click_button_replace=''):
        """
        元素点击

        :click_button: 按钮元素名称，element_locating中option
        """
        if click_button_replace == '':
            self.ele_find(self.page_name, click_button).click()
        elif click_button_replace != '':
            click_button_replace = click_button_replace.strip('<>')
            self.ele_find(self.page_name, click_button, replace_str=click_button_replace).click()

    def dropdown_menu_select(self, selector, target_option, selector_replace='', target_option_repalce=''):
        """
        下拉列表选择

        :selector: 下拉列表元素名称，element_locating中option
        :target_option: 选项名称，element_locating中option
        """
        if selector_replace != '':
            selector_replace = selector_replace.strip('<>')
            self.ele_find(self.page_name, selector, replace_str=selector_replace).click()
        elif selector_replace == '':
            self.ele_find(self.page_name, selector).click

        if target_option_repalce != '':
            target_option_repalce = target_option_repalce.strip('<>')
            self.ele_find(self.page_name, target_option, replace_str=target_option_repalce)
        elif target_option_repalce == '':
            self.ele_find(self.page_name, target_option).click()
        
    def input_send(slef, input, input_content, input_ele_repalce=''):
        """
        输入框输入

        :input: 输入元素名称，element_locating中option
        :input_content: 输入内容
        """
        if input_ele_repalce == '':
            input_ele = slef.ele_find(slef.page_name, input)
        elif input_ele_repalce != '':
            input_ele_repalce = input_ele_repalce.strip('<>')
            input_ele = slef.ele_find(slef.page_name, input, replace_str=input_ele_repalce)
        ActionChains(slef.driver).click(input_ele).send_keys(input_content).perform