import os
from configparser import ConfigParser
from scripts.constants import FILE_CONFIG_DIR, CONFIG_DIR, USER_CONFIG_DIR


class ConfigHandle(ConfigParser):
    """
    封装配置文件操作
    方法1.使用__call__()函数，通过对象(参数)调用__call__()
    载入配置文件
    读取区域，返回字典
    读取选项，转换布尔值，使用eval函数，转换数字型，不做转换返回字符串
    """
    def __init__(self, filename=None):
        super(ConfigHandle, self).__init__()
        self.filename = filename
        # self.read(self.filename, encoding='utf8')

    def __call__(self, section='DEFAULT', option=None, isboolean=False, iseval=False):
        self.read(self.filename, encoding='utf8')
        if option is None:
            try:
                return dict(self[section])  # 返回区域字典，包括默认区域
            except KeyError as e:
                print("传入的区域名不存在！")
                raise e

        if isinstance(isboolean, bool):
            if isboolean:
                try:
                    return self.getboolean(section, option)  # 返回布尔型选项值
                except ValueError as v:
                    print("选项值非布尔类型！")
                    raise v
                except KeyError as k:
                    print("传入的区域名或选项名不存在！")
                    raise k
        else:
            raise ValueError("isboolean类型错误，必须为布尔类型")

        data1 = self.get(section, option)  # 取值原始数据
        if isinstance(iseval, bool):
            if iseval:
                try:
                    return eval(data1)
                except NameError as n:
                    print("选项值类型无法被python识别!")
                    raise n
        else:
            raise ValueError("iseval必须为布尔类型")

        if data1.isdigit():
            return int(data1)
        try:
            return float(data1)
        except ValueError:  # data1不是浮点型则捕获异常
            pass
        return data1  # 对非数字型字符串不做处理，直接返回

    @classmethod
    def write_config(cls, filename, data):
        one_config = cls()  # 创建新的配置文件对象
        for key in data:
            one_config[key] = data[key]
        filename = os.path.join(CONFIG_DIR, filename)  # 路径写死，全都写在logs文件夹下
        with open(filename, 'w', encoding='utf8') as file:
            one_config.write(file)


do_config = ConfigHandle(FILE_CONFIG_DIR)  # 处理配置文件file_con.ini
user_config = ConfigHandle(USER_CONFIG_DIR)  # 处理配置文件user.conf


if __name__ == '__main__':
    a = do_config('excel', 'columns', iseval=True)
    print(a)






