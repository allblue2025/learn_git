import pymysql
import random
from scripts.confighandler import do_config


class MysqlHandler(object):
    """封装pymysql常用操作"""
    def __init__(self):
        self.conn = pymysql.connect(host=do_config('mysql', 'host'),
                                    port=do_config('mysql', 'port'),
                                    user=do_config('mysql', 'user'),
                                    password=do_config('mysql', 'password'),
                                    db=do_config('mysql', 'db'),
                                    charset=do_config('mysql', 'charset'),
                                    cursorclass=pymysql.cursors.DictCursor)  # 建立连接，创建connection对象
        self.cursor = self.conn.cursor()  # 实例化游标对象，作为实例属性

    def __call__(self, sql, args=None, is_all=False):  # args seq
        self.cursor.execute(sql, args)
        self.conn.commit()
        if is_all:
            result = self.cursor.fetchall()  # 返回所有记录
        else:
            result = self.cursor.fetchone()  # 返回第一条记录
        return result

    def close(self):
        """关闭游标和连接"""
        self.cursor.close()
        self.conn.close()

    @staticmethod
    def effective_phone():
        """随机生成手机号"""
        # 第二位数字
        second = [3, 4, 5, 7, 8][random.randint(0, 4)]
        # 第三位数字
        third = {3: random.randint(0, 9),
                 4: [5, 7][random.randint(0, 1)],
                 5: [i for i in range(10) if i != 4][random.randint(0, 8)],
                 7: [i for i in range(10) if i not in [4, 9]][random.randint(0, 7)],
                 8: random.randint(0, 9)}[second]
        # 最后八位数字
        one_str = "1234567890"
        eight_num = ''.join(random.sample(one_str, 8))  # random.sample(seq，n)从序列里随机取样n次组成列表
        # 拼接手机号
        return "1{}{}{}".format(second, third, eight_num)

    def is_existed_mobile(self, phone):
        """生成的手机号查库判断是否存在"""
        sql = "SELECT `Id` FROM future.`member` WHERE `MobilePhone`=%s"
        if self(sql, args=(phone,)):
            return True
        else:
            return False

    def create_unregist_phone(self):
        """生成未注册的手机号"""
        while True:
            a = self.effective_phone()
            if not self.is_existed_mobile(a):  # 返回数据库中没有的手机号
                return a


sql_handle = MysqlHandler()  # 实例化MysqlHandler类

if __name__ == '__main__':
    sql2 = 'select Id from member where "mobilephone" ='
    result1 = sql_handle(sql2, (1,))
    print(result1)
    sql_handle.close()
