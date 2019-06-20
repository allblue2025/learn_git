import unittest
import time
import os
from libs import HTMLTestRunnerNew
from scripts.confighandler import do_config
from scripts.MysqlHandler import sql_handle
from scripts.new_user import create_user_config
from scripts.constants import CASE_DIR, REPORT_DIR, USER_CONFIG_DIR


suite = unittest.defaultTestLoader.discover(CASE_DIR, pattern="test_*.py")


def is_conf_exist():
    if not os.path.exists(USER_CONFIG_DIR):  # 配置文件路径不存在则写入
        create_user_config()  # 函数直接将生成的用户信息写入配置文件
        # ConfigHandle().write_config("user.conf", create_user_config())


def main():
    now = time.strftime("%Y-%m-%d %H_%M_%S")
    filename = REPORT_DIR + '/' + now + do_config("report", "html_report_name")
    file = open(filename, 'wb')
    runner = HTMLTestRunnerNew.HTMLTestRunner(stream=file, verbosity=do_config("report", "verbosity"),
                                              title=do_config("report", "title"),
                                              description=do_config("report", "description"),
                                              tester=do_config("report", "tester"))
    runner.run(suite)
    file.close()  # 关闭文件对象


if __name__ == "__main__":
    is_conf_exist()
    main()




