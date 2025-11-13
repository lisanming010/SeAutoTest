import configparser
import selenium.common.exceptions as seEception
from functools import wraps

def ele_selector_exception_handing(func):
    '''
    监测元素选择情况，并输出日志
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger = args[0].logger #获取元素选择方法类的self.looger日志记录器
        try:
            ele_selector, ele_name = func(*args, **kwargs)
        except FileNotFoundError as e:
            logger.error(f"文件不存在:\n{e}")
            raise e
        except configparser.NoSectionError as e:
            logger.error(f"配置文件读取失败：\n{e}")
            raise e
        except configparser.NoOptionError as e:
            logger.error(f"配置文件读取失败：\n{e}")
            raise e
        except Exception as e:
            logger.error(f"定位失败，捕获错误：\n{e}")
            raise e
        else:
            # find_elements 定位不到元素时返回空白列表而不会抛出错误，为与后续逻辑兼容手动抛出NoSuchElementException
            if ele_selector == []:
                logger.error(f'find_elements返回列表为空，未定位到元素！')
                raise seEception.NoSuchElementException
            logger.info(f"{ele_name}: 元素定位成功！")
            return ele_selector
    return wrapper