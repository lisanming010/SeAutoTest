import os
from pathlib import Path
from utils.confing_handle import HandleConfig

GLOBAL_SETTING_FILE = 'setting.ini'
GLOBAL_CONFIG_PATH = Path(os.getenv("GLOBAL_SETTIGN_CONFIG_PATH", GLOBAL_SETTING_FILE)).expanduser().resolve()

PYTEST_SETTING_FILE = 'pytest.ini'
PYTEST_CONFIG_PATH = Path(os.getenv("PYTEST_SETTIGN_CONFIG_PATH", PYTEST_SETTING_FILE)).expanduser().resolve()

cfg_global = HandleConfig(GLOBAL_CONFIG_PATH)
cfg_pytest = HandleConfig(PYTEST_CONFIG_PATH)