import requests
import json
from scripts.loggerhandler import do_logger


class HttpRequests(object):
    """封装requests库常用操作"""
    def __init__(self):
        self.sessions = requests.Session()  # 实例化Session对象，管理cookie

    def __call__(self, method, url, data=None, isjson=False, **kwargs):
        method = method.upper()
        if isinstance(data, str):   # 对data参数的字符串类型进行判断处理，可能是json格式，也有可能是加引号的字典
            try:
                data = json.loads(data)
            except Exception as e:
                do_logger.info(e)
                data = eval(data)  # eval函数处理字符串
        if method == 'GET':  # get类型请求
            self.response = self.sessions.request('GET', url, params=data, **kwargs)
        elif method == 'POST':  # post类型请求
            if isjson:  # 判断参数是否以json格式传递
                self.response = self.sessions.request('POST', url, json=data, **kwargs)
            else:  # 参数以form表单传递
                self.response = self.sessions.request('POST', url, data=data, **kwargs)
        elif method in ('PUT', 'PATCH'):  # # 处理put，patch等有参数类型的请求
            self.response = self.sessions.request(method, url, data=data, **kwargs)
        else:
            self.response = self.sessions.request(method, url, **kwargs)  # 处理delete，options,head等其他无参数类型的请求

        return self.response

    def close(self):  # 关闭Session对象
        self.sessions.close()

    def detail(self):  # 查看响应内容：状态码，响应正文，cookie值
        return self.response.status_code, self.response.json(), self.response.cookies

# one_request = HttpRequests()


def main():
    do_logger.info("wwww")
    base_url = "http://test.lemonban.com:8080/futureloan/mvc/api"
    phone = '13921000030'
    register_url = base_url + "/member/register"
    register_data = {"mobilephone": phone, "pwd": "12345678", "regname": None}
    login_url = base_url + "/member/login"
    login_data = {"mobilephone": phone, "pwd": "12345678"}
    recharge_url = base_url + "/member/recharge"
    recharge_data = {"mobilephone": "13923000000", "amount": "<html>"}
    add_url = base_url + "/loan/add"
    #add_data = {"memberId": "wwwww", "title": "1111", "amount": "1000", "loanRate": 5,
    #           "loanTerm": 6, "loanDateType": 0, "repaymemtWay": 4, "biddingDays": 7}
    add_data = {"memberId": 7912, "title": "daikuan", "amount": 10000.00, "loanRate": 5.5,
                "loanTerm": 6, "loanDateType": 2, "repaymemtWay": 4, "biddingDays": 0}

    one_request = HttpRequests()  # 实例化HttpRequests类
    a = one_request('get', register_url, register_data)  # 发起注册请求
    print(a.json())
#    do_logger.debug(str(one_request.detail()))  # 显示返回的注册响应结果
#     one_request('POST', login_url, login_data)  # 发起登陆请求
#     do_logger.debug(str(one_request.detail()))  # 显示返回的登陆响应结果
    # one_request('PoST', recharge_url, recharge_data)  # 发起充值请求
    # do_logger.debug(str(one_request.detail()))  # 显示返回的充值响应结果
    # one_request('post', add_url, add_data)  # 发起添加项目请求
    # do_logger.debug(str(one_request.detail()))  # 显示返回的登陆响应结果
    one_request.close()  # 关闭session对象


if __name__ == '__main__':
        main()


