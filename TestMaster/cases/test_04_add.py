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
class TestAdd(unittest.TestCase):
    base_url = do_config("interface", "base_url")
    add_excel = ExcelHandler(CASE_DATA_DIR, 'add')

    @classmethod
    def setUpClass(cls):
        cls.one_request = HttpRequests()
        cls.do_mysql = MysqlHandler()
        do_logger.info("\n{:=^50s}" .format("开始执行加标接口用例"))

    @classmethod
    def tearDownClass(cls):
        cls.one_request.close()
        do_logger.info("\n{:=^50s}" .format("执行加标接口用例结束"))
        cls.do_mysql.close()

    @data(*add_excel.read_excel())
    def test_login(self, nt):
        case_id = nt.case_id
        url = self.base_url + nt.url
        data1 = ReText.add_parametrization(nt.data)
        check_sql = nt.check_sql
        if check_sql:
            sql = ReText.add_parametrization(check_sql)
            before_id = self.do_mysql(sql)['Id']  # 查库取出加标前最大id，可能是null
        actual_response = self.one_request(nt.method, url, data1)  # 发起加标请求
        try:  # 判断状态码是否200，异常状态不用做返回值的断言
            self.assertEqual(200, actual_response.status_code,
                             msg="测试【{}】时，请求失败！状态码为【{}】" .format(nt.title, actual_response.status_code))
        except AssertionError as e:
            do_logger.error('用例执行失败!具体异常为：{}' .format(e))
            self.add_excel.write_excel(case_id+1, actual_response.text, do_config("msg", "fail_msg"))
            raise e

        try:
            self.assertEqual(json.loads(nt.expected, encoding='utf8'), actual_response.json(), msg="执行[{}]失败" .format(nt.title))
            if check_sql:
                sql = ReText.add_parametrization(check_sql)
                after_id = self.do_mysql(sql)['Id']  # 查库取出加标后最大id
                # 最大标id不一致，则表明数据插入成功，断言成功
                self.assertNotEqual(before_id, after_id,
                                    msg="执行[{}]失败，数据库中插入加标记录失败！" .format(nt.title))
        except AssertionError as e:
            do_logger.error('用例执行失败!具体异常为：{}' .format(e))
            self.add_excel.write_excel(case_id+1, actual_response.text, do_config("msg", "fail_msg"))
            raise e
        else:
            self.add_excel.write_excel(case_id+1, actual_response.text, do_config("msg", "pass_msg"))


if __name__ == '__main__':
    unittest.main()
