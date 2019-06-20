import unittest
from scripts.HttpRequests import HttpRequests
from libs.ddt import ddt, data
from scripts.excelhandler import ExcelHandler
from scripts.ReHandler import ReText
from scripts.loggerhandler import do_logger
from scripts.confighandler import user_config, do_config
from scripts.MysqlHandler import MysqlHandler
from scripts.constants import CASE_DATA_DIR


@ddt
class TestRecharge(unittest.TestCase):
    base_url = do_config("interface", "base_url")
    recharge_excel = ExcelHandler(CASE_DATA_DIR, 'recharge')

    @classmethod
    def setUpClass(cls):
        cls.one_request = HttpRequests()
        user_data = {"mobilephone": user_config("invest_user", "phone"), "pwd": user_config("invest_user", "pwd")}
        cls.one_request('post', cls.base_url+'/member/login', user_data)
        cls.do_mysql = MysqlHandler()
        do_logger.info("\n{:=^50s}" .format("开始执行充值接口用例"))

    @classmethod
    def tearDownClass(cls):
        cls.one_request.close()
        do_logger.info("\n{:=^50s}" .format("执行充值接口用例结束"))
        cls.do_mysql.close()

    @data(*recharge_excel.read_excel())
    def test_login(self, nt):
        case_id = nt.case_id
        url = self.base_url + nt.url
        data1 = ReText.recharge_parametrization(nt.data)
        check_sql = nt.check_sql
        if check_sql:
            sql = ReText.recharge_parametrization(check_sql)
            # sql = "SELECT `LeaveAmount` FROM future.`member` WHERE `Id`=%s"

            before_amount = self.do_mysql(sql)['LeaveAmount']  # 查库取出投资人充值前的金额,是Decimal类型，需要转换类型
            before_amount = round(float(before_amount), 2)
        actual_response = self.one_request(nt.method, url, data1)  # 发起充值请求
        try:  # 判断状态码是否200，异常状态不用做返回值的断言
            self.assertEqual(200, actual_response.status_code,
                             msg="测试【{}】时，请求失败！状态码为【{}】" .format(nt.title, actual_response.status_code))
        except AssertionError as e:
            do_logger.error('用例执行失败!具体异常为：{}' .format(e))
            self.recharge_excel.write_excel(case_id+1, actual_response.text, do_config("msg", "fail_msg"))
            raise e

        try:
            self.assertIn(nt.expected, actual_response.text, msg="执行[{}]失败" .format(nt.title))  # assertIn必须是两个序列类型
            if check_sql:
                sql = ReText.recharge_parametrization(check_sql)
                after_amount = self.do_mysql(sql)['LeaveAmount']  # 查库取出投资人充值前的金额,是Decimal类型，需要转换类型
                after_amount = round(float(after_amount), 2)
                expect_amount = eval(data1).get('amount')  # data1为字符串类型的字典, get期望充值金额
                actual_amount = round(after_amount - before_amount, 2)  # 实际充值金额

                self.assertEqual(expect_amount, actual_amount,
                                 msg="执行[{}]失败，数据库中充值的金额错误，期望充值{}，实际充值{}" .format(nt.title,
                                                                                                            expect_amount,
                                                                                                            actual_amount))
        except AssertionError as e:
            do_logger.error('用例执行失败!具体异常为：{}' .format(e))
            self.recharge_excel.write_excel(case_id+1, actual_response.text, do_config("msg", "fail_msg"))
            raise e
        else:
            self.recharge_excel.write_excel(case_id+1, actual_response.text, do_config("msg", "pass_msg"))


if __name__ == '__main__':
    unittest.main()


