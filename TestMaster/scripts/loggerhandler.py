import logging
import os
from logging.handlers import RotatingFileHandler
from scripts.confighandler import do_config  # 日志配置文件操作对象
from scripts.constants import LOG_DIR
from concurrent_log_handler import ConcurrentRotatingFileHandler  # 日志的准确性无法保证，所以改用进程安全


class LoggerHandler:
    """
    封装日志操作
    """
    def __init__(self, isconsole=True):
        self.logger = logging.getLogger(do_config('log', 'logger_name'))  # 1 定义日志器的名字
        self.logger.setLevel(logging.DEBUG)  # 2 指定日志收集器的日志等级
        file_log_dir = os.path.join(LOG_DIR, do_config("log", "log_file_name"))  # 日志文件路径
        # 有bug，PermissionError：[WinError 32] 另一个程序正在使用日志文件
        # 解决方案1：每个模块都实例化一个日志器对象
        # 方案2 安装并导入第三方模块 pip install concurrent-log-handler
        # file_handle = RotatingFileHandler(file_log_dir,
        #                                   maxBytes=do_config('log', 'maxBytes'),
        #                                   backupCount=do_config('log', 'backupCount'), encoding='utf8')  # 3 定义文件handle对象,日志回滚
        file_handle = ConcurrentRotatingFileHandler(file_log_dir,
                                                    maxBytes=do_config('log', 'maxBytes'),
                                                    backupCount=do_config('log', 'backupCount'), encoding='utf8')  # 3 定义文件handle对象,日志回滚
        file_handle.setLevel(do_config('log', 'file_handle_level'))  # 4 指定文件handle对象的日志等级
        formatter = logging.Formatter(do_config('log', 'formatter'))  # 5 定义日志格式对象
        file_handle.setFormatter(formatter)  # 6 设置文件handle格式
        self.logger.addHandler(file_handle)  # 7 日志收集器与handle对接
        if isinstance(isconsole, bool):
            if isconsole:
                console_handle = logging.StreamHandler()  # 定义控制台handle对象
                console_handle.setLevel(do_config('log', 'console_handle_level'))  # 设置控制台handle对象的日志等级
                console_handle.setFormatter(formatter)  # 设置控制台handle格式
                self.logger.addHandler(console_handle)  # 日志收集器与控制台handle对接
        else:
            raise ValueError("isconsole为布尔类型")

    def get_logger(self):
        """
        返回日志收集器对象
        :return:
        """
        return self.logger


do_logger = LoggerHandler().get_logger()

if __name__ == '__main__':
    for _ in range(100):
        do_logger.info("这是DUBUG日志")
        do_logger.warning("这是warning日志")
        do_logger.critical("这是critical日志")
        do_logger.error("这是error日志")
