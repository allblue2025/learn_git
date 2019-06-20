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
    register_excel = ExcelHandler(CASE_DATA_DIR, 'register')

    @classmethod
    def setUpClass(cls):
        cls.one_request = HttpRequests()
        do_logger.info("\n{:=^50s}" .format("开始执行注册接口用例"))

    @classmethod
    def tearDownClass(cls):
        cls.one_request.close()
        do_logger.info("\n{:=^50s}" .format("执行注册接口用例结束"))

    @data(*register_excel.read_excel())
    def test_register(self, nt):
        case_id = nt.case_id
        url = self.base_url + nt.url
        data1 = ReText.register_parametrization(nt.data)  # 正则参数化data数据
        expected = json.loads(nt.expected)
        actual = self.one_request(nt.method, url, data1)  # 发起注册请求
        try:
            self.assertEqual(expected, actual.json(), msg="执行[{}]失败" .format(nt.title))
        except AssertionError as e:
            do_logger.error('用例执行失败!具体异常为：{}' .format(e))
            self.register_excel.write_excel(case_id+1, actual.text, do_config("msg", "fail_msg"))
            raise e
        else:
            self.register_excel.write_excel(case_id+1, actual.text, do_config("msg", "pass_msg"))


if __name__ == '__main__':
    unittest.main()

