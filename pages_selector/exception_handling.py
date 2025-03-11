def ele_selector_exception_handing(func):
    '''
    监测元素选择情况，并输出日志
    '''
    def wrapper(*args, **kwargs):
        logger = args[0].logger #获取元素选择方法类的self.looger日志记录器
        try:
            ele_selector = func(*args, **kwargs)
        except Exception as e:
            print(logger)
            logger.error(f"元素定位错误：{e}")
            raise
        else:
            logger.info(f"元素定位成功！")
        return ele_selector
    return wrapper