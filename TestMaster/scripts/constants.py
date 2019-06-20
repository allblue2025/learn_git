from os.path import dirname, abspath, join

# 获取项目根目录路径
BASE_DIR = dirname(dirname(abspath(__file__)))  # __file__固定变量
a = __file__

# 获取测试数据datas所在目录的路径
DATA_DIR = join(BASE_DIR, "datas")

# 获取config配置文件所在目录的路径
CONFIG_DIR = join(BASE_DIR, "configs")

LOG_DIR = join(BASE_DIR, "logs")

REPORT_DIR = join(BASE_DIR, "reports")

CASE_DIR = join(BASE_DIR, "cases")  # 用例路径

FILE_CONFIG_DIR = join(CONFIG_DIR, "file_con.ini")  # 配置文件路径

USER_CONFIG_DIR = join(CONFIG_DIR, "user.conf")  # 用户账号配置文件路径

CASE_DATA_DIR = join(DATA_DIR, "cases.xlsx")  # excel文件路径



