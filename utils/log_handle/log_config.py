import os

def log_conf_dict(log_file_name, log_file_path):
    '''
    生成日志配置字典
    :log_file_path:日志文件存储路径,默认为项目路径下logs文件夹
    :log_file_name:日志文件名称,同时也用作日志记录器名称
    '''
    
    log_file_full_path = os.path.join(log_file_path, log_file_name)

    # 日志配置字典
    loggin_dic = {
        'version': 1.0,
        'disable_existing_loggers': False,
        # 日志格式
        'formatters': {
            'standard': {
                'format': '%(asctime)s %(threadName)s:%(thread)d [%(name)s] %(levelname)s [%(pathname)s:%(lineno)d] %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S',
            },
            'simple': {
                'format': '%(asctime)s [%(name)s] %(levelname)s  %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S',
            },
            'test': {
                'format': '%(asctime)s %(message)s',
            }
        },
        'filters': {},
        # 日志处理器
        'handlers': {
            'console_debug_handler': {
                'level': 'DEBUG',  # 日志处理的级别限制
                'class': 'logging.StreamHandler',  # 输出到终端
                'formatter': 'simple'  # 日志格式
            },
            'file_info_handler': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件,日志轮转
                'filename': log_file_full_path,
                'maxBytes': 1024 * 1024 * 10,  # 日志大小 10M
                'backupCount': 1000,  # 日志文件保存数量限制
                'encoding': 'utf-8',
                'formatter': 'standard',
            }
        },
        # 日志记录器
        'loggers': {
            '': {
                'handlers': ['console_debug_handler', 'file_info_handler'],
                'level': 'DEBUG',
                'propagate': False,
            },
        }
    }
    return loggin_dic
