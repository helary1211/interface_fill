# _*_ encoding:utf-8 _*_
# @Time : 2020/7/5 10:21
# @Author : chenmeihuan
# @File : test_login.py
# @Software: PyCharm
import pytest
from core.client import *
from core.util import *
# @pytest.mark.parametrize('username,password,error_code,msg',
#                          [('zhangsan','MTIzMTIzNDU2',0,'登录成功'),
#                           ( 'zhangsan','123456',10000,'密码错误'),
#                           ('zhangsan','',10001,'密码为空')])
@params('username,password,error_code,msg',csv('login.csv'))
@feature('登录接口')
@title('登录数据测试')
@order(order=1)
def test_login01(client,username, password, error_code,msg):
    '''
    登录数据测试
    :return:
    '''
    # client = Client(url="event/api/login/",method=METHOD.POST,body_type=BODY_TYPE.FORM)
    client.set_bodys({"username":username, "password":password})
    client.send()
    client.check_status_code(200)
    client.check_res_times_less_than(1000)
    client.check_json_value('error_code',error_code)

def test_login02(client):
    '''
    正常登录，校验uid
    :return:
    '''
    client.set_bodys({"username":"zhangsan", "password":"MTIzMTIzNDU2"})
    client.send()
    client.check_status_code(200)
    client.check_res_times_less_than(1000)
    client.check_mysql_value('select user_id from api_userdetail where phone=13800000001','uid')
