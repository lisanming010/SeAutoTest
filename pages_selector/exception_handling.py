import configparser

def ele_selector_exception_handing(func):
    '''
    监测元素选择情况，并输出日志
    '''
    def wrapper(*args, **kwargs):
        logger = args[0].logger #获取元素选择方法类的self.looger日志记录器
        try:
            ele_selector = func(*args, **kwargs)
        except FileNotFoundError as e:
            logger.error(f"文件不存在：{e}")
        except configparser.NoSectionError as e:
            logger.error(f"配置文件读取失败：{e}")
        except configparser.NoOptionError as e:
            logger.error(f"配置文件读取失败：{e}")
        except Exception as e:
            logger.error(f"捕获错误：{e}")
        else:
            logger.info(f"元素定位成功！")
            return ele_selector
    return wrapper