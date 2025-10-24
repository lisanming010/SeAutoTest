### 0.env
- python 3.9

### 1. 项目架构

``````
.
├── Pipfile
├── Pipfile.lock
├── README.md
├── conftest.py		全局pytest conftest
├── config.py       配置文件读取单例入口
├── logs			日志存放位置
├── main.py			程序入口
├── pages_selector	元素定位封装
│   ├── element_locating.ini	元素定位名称-xpath关系映射配置文件
│   ├── exception_handling.py	元素定位执行装饰器，目前仅捕获定位错误并输出日志
│   └── find_element.py			元素定位方法封装
├── pytest.ini		pytest配置文件
├── result			结果存放文件夹
├── screenshots		错误截图存放文件夹
├── setting.ini		全局配置文件
├── test_cases		测试用例文件夹
│   ├── login_test	登录验证
│   │   └── test_login.py
│   └── vm_test		虚拟机相关测试用例
│       ├── conftest.py	虚拟机相关用例
│       ├── test_vm_create.py	虚拟机相关测试用例编排入口
│       └── vm_assert_check.py	虚拟机相关测试用例断言检测封装
└── utils			工具类
    ├── confing_handle.py	配置文件处理封装
    ├── ele_action.py		Se元素动作封装
    ├── log_handle			日志相关方法封装
    │   ├── log_config.py	日志配置
    │   └── log_handle.py	日志方法封装
    ├── ssh_env.py			ssh工具封装
    └── tools.py			杂项方法封装
``````



