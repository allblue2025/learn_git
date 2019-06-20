import unittest
import json
from scripts.HttpRequests import HttpRequests
from libs.ddt import ddt, data
from scripts.excelhandler import ExcelHandler
from scripts.ReHandler import ReText
from scripts.loggerhandler import do_logger
from scripts.confighandler import do_config
from scripts.constants import CASE_DATA_DIR


@ddt
class TestRegister(unittest.TestCase):
    base_url = do_config("interface", "base_url")
    login_excel = ExcelHandler(CASE_DATA_DIR, 'login')

    @classmethod
    def setUpClass(cls):
        cls.one_request = HttpRequests()
        do_logger.info("\n{:=^50s}" .format("开始执行登录接口用例"))

    @classmethod
    def tearDownClass(cls):
        cls.one_request.close()
        do_logger.info("\n{:=^50s}" .format("执行登录接口用例结束"))

    @data(*login_excel.read_excel())
    def test_login(self, nt):
        case_id = nt.case_id
        url = self.base_url + nt.url
        data1 = ReText.login_parametrization(nt.data)
        expected = json.loads(nt.expected)
        actual = self.one_request(nt.method, url, data1)
        try:
            self.assertEqual(expected, actual.json(), msg="执行[{}]失败" .format(nt.title))
        except AssertionError as e:
            do_logger.error('用例执行失败!具体异常为：{}' .format(e))
            self.login_excel.write_excel(case_id+1, actual.text, do_config("msg", "fail_msg"))
            raise e
        else:
            self.login_excel.write_excel(case_id+1, actual.text, do_config("msg", "pass_msg"))


if __name__ == '__main__':
    unittest.main()
