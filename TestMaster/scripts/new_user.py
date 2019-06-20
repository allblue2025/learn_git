from scripts.HttpRequests import HttpRequests
from scripts.MysqlHandler import MysqlHandler
from scripts.confighandler import do_config
import json


def create_new_user(regname, pwd="12345678"):
    handle_mysql = MysqlHandler()
    request = HttpRequests()
    sql = "SELECT `Id` FROM future.`member` WHERE `MobilePhone`=%s"
    url = do_config('interface', 'base_url') + "/member/register"
    while True:
        phone = handle_mysql.create_unregist_phone()
        data = {"mobilephone": phone, "pwd": pwd, "regname": regname}
        request('post', url, data)
        result = handle_mysql(sql, (phone,))
        if result:
            id = result['Id']
            break
    user_dict = {
        regname: {
            'id': id,
            'regname': regname,
            'pwd': pwd,
            'phone': phone
        }
    }
    request.close()
    handle_mysql.close()
    return user_dict


def create_user_config():
    users_dict = {}
    users_dict.update(create_new_user('manage_user'))
    users_dict.update(create_new_user('invest_user'))
    users_dict.update(create_new_user('borrow_user'))
    do_config.write_config("user.conf", users_dict)
    # return users_dict


if __name__ == '__main__':
    create_user_config()


