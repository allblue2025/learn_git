import requests

url = "https://www.zhihu.com/signin?next=%2F"
data = {'phoneNo': 15292934567}
sessions = requests.Session()  # 实例化Session对象，管理cookie
reponse = sessions.request('post', url, data)
print(reponse.text)
