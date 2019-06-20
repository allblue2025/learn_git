import re
import random
from scripts.MysqlHandler import MysqlHandler
from scripts.confighandler import ConfigHandle
from scripts.constants import USER_CONFIG_DIR


class ReText(object):
    do_config = ConfigHandle(USER_CONFIG_DIR)
    """用re正则替换文本中的指定数据"""
    # 1 将正则字符串编译成Pattern对象,r只能转义\
    unreg_pattern = re.compile(r"\$\{unregister_phone\}")  # 未注册手机号匹配
    null_id_pattern = re.compile(r"\$\{null_id\}")  # 不存在的用户id匹配
    null_loan_id_pattern = re.compile(r"\$\{null_loan_id\}")  # 不存在的标id匹配
    loan_id_pattern = re.compile(r"\$\{loan_id\}")  # 已有标id匹配
    ill_pattern = re.compile(r"\$\{illegal_phone\}")  # 非法手机号匹配
    invest_phone_pattern = re.compile(r"\$\{invest_phone\}")  # 投资人手机号匹配
    invest_pwd_pattern = re.compile(r"\$\{invest_pwd\}")  # 投资人密码匹配
    invest_id_pattern = re.compile(r"\$\{invest_id\}")  # 投资人id匹配
    manage_phone_pattern = re.compile(r"\$\{manage_phone\}")  # 管理员手机号匹配
    manage_pwd_pattern = re.compile(r"\$\{manage_pwd\}")  # 管理员密码匹配
    manage_id_pattern = re.compile(r"\$\{manage_id\}")  # 管理员id匹配
    borrow_phone_pattern = re.compile(r"\$\{borrow_phone\}")  # 借款人手机号匹配
    borrow_id_pattern = re.compile(r"\$\{borrow_id\}")  # 借款人id匹配
    # borrow_pwd_pattern = re.compile(r"\$\{borrow_pwd\}")  # 借款人密码匹配

    @classmethod
    def unregister_phone_replace(cls, data):
        """
        正则替换excel中未注册的手机号
        :param data: str包含${unregister_phone}
        :return:
        """
        if re.search(cls.unreg_pattern, data):
            do_mysql = MysqlHandler()
            phone = do_mysql.create_unregist_phone()
            data = re.sub(cls.unreg_pattern, phone, data)  # 替换成数据库没有记录的随机手机号,sub()第二个第三个参数必须是字符串
            do_mysql.close()  # 关闭数据库连接
        return data

    @classmethod
    def illegal_phone_replace(cls, data):
        """
        正则替换excel中非法手机号
        :param data: str包含${illegal_phone}
        :return:
        """
        if re.search(cls.ill_pattern, data):
            data = re.sub(cls.ill_pattern, cls.illegal_phone(), data)  # 替换成随机非法手机号
        return data

    @classmethod
    def invest_phone_replace(cls, data):
        """
        正则替换excel中投资人手机号,密码
        :param data: str包含${invent_phone},${invent_pwd},${invent_id}
        :return:
        """
        if re.search(cls.invest_phone_pattern, data):
            data = re.sub(cls.invest_phone_pattern, str(cls.do_config("invest_user", "phone")), data)  # 替换成投资人手机号
        if re.search(cls.invest_pwd_pattern, data):
            data = re.sub(cls.invest_pwd_pattern, str(cls.do_config("invest_user", "pwd")), data)  # 替换成投资人密码
        if re.search(cls.invest_id_pattern, data):
            data = re.sub(cls.invest_id_pattern, str(cls.do_config("invest_user", "id")), data)  # 替换成投资人id
        return data

    @classmethod
    def manage_phone_replace(cls, data):
        """
        正则替换excel中管理员手机号,密码
        :param data: str包含${manage_phone}，${manage_pwd}，${manage_id}
        :return:
        """
        if re.search(cls.manage_phone_pattern, data):
            data = re.sub(cls.manage_phone_pattern, str(cls.do_config("manage_user", "phone")), data)  # 替换成管理员手机号
        if re.search(cls.manage_pwd_pattern, data):
            data = re.sub(cls.manage_pwd_pattern, str(cls.do_config("manage_user", "pwd")), data)  # 替换成管理员密码
        if re.search(cls.manage_id_pattern, data):
            data = re.sub(cls.manage_id_pattern, str(cls.do_config("manage_user", "id")), data)  # 替换管理员id
        return data

    @classmethod
    def borrow_phone_replace(cls, data):
        """
        正则替换excel中借款人手机号,id
        :param data: str包含${borrow_phone}，${borrow_id}
        :return:
        """
        if re.search(cls.borrow_phone_pattern, data):
            data = re.sub(cls.borrow_phone_pattern, str(cls.do_config("borrow_user", "phone")), data)  # 替换成借款人手机号
        if re.search(cls.borrow_id_pattern, data):
            data = re.sub(cls.borrow_id_pattern, str(cls.do_config("borrow_user", "id")), data)  # 替换成借款人id
        # if re.search(self.borrow_pwd_pattern, data):
        #     data = re.sub(self.borrow_pwd_pattern, do_config("borrow_user", "pwd"), data)  # 替换成借款人密码
        return data

    @classmethod
    def null_id_replace(cls, data):
        """
        正则替换excel中不存在的用户id
        :param data: str包含${null_id}
        :return:
        """
        if re.search(cls.null_id_pattern, data):
            do_mysql = MysqlHandler()
            sql = "SELECT `Id` FROM future.`member`ORDER BY `Id` DESC LIMIT 1;"
            unexist_id = do_mysql(sql=sql).get('Id') + 100  # 获取最大id+100，即不存在的用户id
            data = re.sub(cls.null_id_pattern, str(unexist_id), data)  # 替换成数据库没有记录的用户id,sub()第二个第三个参数必须是字符串
            do_mysql.close()  # 关闭数据库连接
        return data

    @classmethod
    def null_loan_id_replace(cls, data):
        """
        正则替换excel中不存在的标id
        :param data: str包含${null_load_id}
        :return:
        """
        if re.search(cls.null_loan_id_pattern, data):
            do_mysql = MysqlHandler()
            sql = "SELECT `Id` FROM future.`loan`ORDER BY `CreateTime` DESC LIMIT 1;"
            unexist_id = do_mysql(sql=sql).get('Id') + 100  # 获取最大id+100，即不存在的标id
            data = re.sub(cls.null_loan_id_pattern, str(unexist_id), data)  # 替换成数据库没有记录的标id,sub()第二个第三个参数必须是字符串
            do_mysql.close()  # 关闭数据库连接
        return data

    @classmethod
    def loan_id_replace(cls, data):
        """
        正则替换excel中已有的标id
        :param data: str包含${load_id}
        :return:
        """
        if re.search(cls.loan_id_pattern, data):
            do_mysql = MysqlHandler()
            sql = "SELECT `Id` FROM future.`loan`ORDER BY `CreateTime` DESC LIMIT 1;"
            # getattr()第一个参数为对象（类），第二个参数为字符串类型的属性名
            # setattr(对象,符串类型的属性名, 属性值)
            loan_id = getattr(cls, "loan_id")  # 获取对象（类）的实例属性值（类属性值）
            data = re.sub(cls.loan_id_pattern, str(loan_id), data)  # 替换成数据库没有记录的标id,sub()第二个第三个参数必须是字符串
            do_mysql.close()  # 关闭数据库连接
        return data

    @classmethod
    def register_parametrization(cls, data):
        """
        注册功能的参数化
        :param data: 参数字典的str类型
        :return:
        """
        # 正则替换未注册的手机号
        data = cls.unregister_phone_replace(data)
        # 替换非法手机号
        data = cls.illegal_phone_replace(data)
        # 替换已注册的投资人手机号和密码
        data = cls.invest_phone_replace(data)

        return data

    @classmethod
    def login_parametrization(cls, data):
        """
        登录功能的参数化
        :param data: 参数字典的str类型
        :return:
        """
        # 正则替换未注册的手机号
        data = cls.unregister_phone_replace(data)
        # 替换已注册的投资人手机号，密码
        data = cls.invest_phone_replace(data)

        return data

    @classmethod
    def recharge_parametrization(cls, data):
        """
        充值功能的参数化
        :param data: 参数字典的str类型
        :return:
        """
        # 替换已注册的投资人手机号
        data = cls.invest_phone_replace(data)
        # 替换已注册的借款人手机号
        data = cls.borrow_phone_replace(data)
        # 正则替换未注册的手机号
        data = cls.unregister_phone_replace(data)
        return data

    @classmethod
    def add_parametrization(cls, data):
        """
        加标功能的参数化
        :param data: 参数字典的str类型
        :return:
        """
        # 替换管理员手机号密码id
        data = cls.manage_phone_replace(data)
        # 替换已注册的借款人id
        data = cls.borrow_phone_replace(data)
        # 正则替换不存在的用户id
        data = cls.null_id_replace(data)
        return data

    @classmethod
    def invest_parametrization(cls, data):
        """
        投标功能的参数化
        :param data: 参数字典的str类型
        :return:
        """
        # 替换管理员手机号密码id
        data = cls.manage_phone_replace(data)
        # 替换已注册的借款人id
        data = cls.borrow_phone_replace(data)
        # 替换已注册的投资人手机号密码id
        data = cls.invest_phone_replace(data)
        # 正则替换不存在的用户id
        data = cls.null_id_replace(data)
        # 正则替换不存在的标id
        data = cls.null_loan_id_replace(data)
        # 正则替换已有的标id
        data = cls.loan_id_replace(data)
        return data

    @staticmethod
    def illegal_phone():
        """随机生成非法手机号"""
        first = random.randint(2, 9)
        one_str = '1234567890'
        end = ''.join(random.sample(one_str, 10))
        return "{}{}" .format(first, end)


if __name__ == '__main__':
    str1 = '{"mobilephone": "${unregister_phone}", "pwd":"${illegal_phone}", "regname": "iris"}'
    str2 = '{"mobilephone": "${invest_phone}", "pwd": "${invest_pwd}", "regname": "${null_loan_id}"}'
    a = ReText.null_loan_id_replace(str2)
    print(a)
    pass





