# _*_ encoding:utf-8 _*_
# @Time : 2020/7/5 10:21
# @Author : chenmeihuan
# @File : test_geteventlist.py
# @Software: PyCharm

from core.client import *
from core.util import *

@feature('查询活动接口')
@title('无条件查询')
@order(order=2)
def test_geteventlist01(get,set,depends):
    '''
    查询所有活动
    :return:
    '''
    uid = depends('login',{"body":{"username":"zhangsan", "password":"MTIzMTIzNDU2"}},'uid')
    client = Client(url="get_eventlist/",method=METHOD.GET,body_type=BODY_TYPE.FORM)
    client.set_params({"rstr":get('rstr')})
    client.set_headers({"uid":uid,"key":get('key')})
    client.send()
    client.check_status_code(200)
    client.check_res_times_less_than(1000)
    client.check_json_value('error_code',0)

    id = client.get_json_value('event_list[0].id')
    set("event_id",id)
    # res = requests.get(url="http://123.56.99.53:9000/event/api/get_eventlist/",
    #               headers={"uid":"4","key":"ab97f63764b608f6d01909d67b4a1c6d"},
    #               params={"rstr":123})
    # print(res.text)
    # assert res.status_code == 200, "响应状态码非200"