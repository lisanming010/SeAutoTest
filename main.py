import pytest
from config import cfg_global, cfg_pytest

SETTIGN_FILE = 'setting.ini'

def make_pytest_conf():
    pytest_conf = cfg_global.read_section('pytest')
    cfg_pytest.conf_write('pytest', pytest_conf)

def update_pytest_conf():
    run_nums = cfg_global.get_value_str('global', 'number_of_process')
    pytest_addopts = cfg_global.get_value_str('pytest', 'addopts')
    value = pytest_addopts + f' -n {run_nums}'
    options = [('addopts', value)]
    cfg_pytest.update_conf('pytest', options)

if __name__ == '__main__':
    make_pytest_conf()
    update_pytest_conf()
    pytest.main()
