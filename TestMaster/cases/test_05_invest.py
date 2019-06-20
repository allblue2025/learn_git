import unittest
import json
from scripts.HttpRequests import HttpRequests
from libs.ddt import ddt, data
from scripts.excelhandler import ExcelHandler
from scripts.ReHandler import ReText
from scripts.loggerhandler import do_logger
from scripts.confighandler import do_config
from scripts.MysqlHandler import MysqlHandler
from scripts.constants import CASE_DATA_DIR


@ddt
class TestInvest(unittest.TestCase):
    base_url = do_config("interface", "base_url")
    invest_excel = ExcelHandler(CASE_DATA_DIR, 'invest')

    @classmethod
    def setUpClass(cls):
        cls.one_request = HttpRequests()
        cls.do_mysql = MysqlHandler()
        do_logger.info("\n{:=^50s}" .format("开始执行投资接口用例"))

    @classmethod
    def tearDownClass(cls):
        cls.one_request.close()
        do_logger.info("\n{:=^50s}" .format("执行投资接口用例结束"))
        cls.do_mysql.close()

    @data(*invest_excel.read_excel())
    def test_invest(self, nt):
        case_id = nt.case_id
        url = self.base_url + nt.url
        data1 = ReText.invest_parametrization(nt.data)
        actual_response = self.one_request(nt.method, url, data1)  # 发起投标请求
        try:  # 判断状态码是否200，异常状态不用做返回值的断言
            self.assertEqual(200, actual_response.status_code,
                             msg="测试【{}】时，请求失败！状态码为【{}】" .format(nt.title, actual_response.status_code))
        except AssertionError as e:
            do_logger.error('用例执行失败!具体异常为：{}' .format(e))
            self.invest_excel.write_excel(case_id + 1, actual_response.text, do_config("msg", "fail_msg"))
            raise e

        if actual_response.json().get('msg') == "加标成功":  # 解决用例对loadid的依赖关系
            check_sql = nt.check_sql
            if check_sql:
                sql = ReText.invest_parametrization(check_sql)
                loan_id = self.do_mysql(sql)['Id']
                # ReText.loan_id = loan_id  # 查库取出加标后最大id，动态为Retext类生成类属性
                # 反射解决了不能互相导包，全局变量值更新的问题
                setattr(ReText, "loan_id", loan_id)  # 反射，动态为对象（类）生成实例属性（类属性）

        expected = json.loads(nt.expected, encoding='utf8')  # 字典类型的期望值
        try:
            self.assertEqual(expected, actual_response.json(), msg="执行[{}]失败" .format(nt.title))
            if expected.get("msg") == "竞标成功":  # 竞标成功的用例，断言数据库投资金额是否正确。用户剩余金额也可以断言，未写
                check_sql = nt.check_sql
                sql = ReText.invest_parametrization(check_sql)
                actual_amount = self.do_mysql(sql).get('Amount')  # 查库取出投资人投资记录,是Decimal类型，需要转换类型
                actual_amount = round(float(actual_amount), 2)
                expect_amount = eval(data1).get('amount')  # data1为字符串类型的字典, get期望充值金额
                self.assertEqual(expect_amount, actual_amount,
                                 msg="执行[{}]失败，数据库中投资的金额错误，期望投资{}，实际投资{}" .format(nt.title,
                                                                                                            expect_amount,
                                                                                                            actual_amount))
        except AssertionError as e:
            do_logger.error('用例执行失败!具体异常为：{}' .format(e))
            self.invest_excel.write_excel(case_id + 1, actual_response.text, do_config("msg", "fail_msg"))
            raise e
        else:
            self.invest_excel.write_excel(case_id + 1, actual_response.text, do_config("msg", "pass_msg"))


if __name__ == '__main__':
    unittest.main()
