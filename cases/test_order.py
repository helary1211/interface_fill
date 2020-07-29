# _*_ encoding:utf-8 _*_
# @Time : 2020/7/5 10:21
# @Author : chenmeihuan
# @File : test_order.py
# @Software: PyCharm
from core.client import *
from core.util import *

@feature('活动预定接口')
@title('预定成功')
@order(order=3)
def test_order01():
    '''
    预定活动成功
    :return:
    '''
    # res = requests.post(url="http://123.56.99.53:9000/event/api/order/",
    #               headers={"Content-Type":"application/x-www-form-urlencoded",
    #                        "uid":"4","key":"ab97f63764b608f6d01909d67b4a1c6d"},
    #               data={"rstr":123,"eid":10})
    # print(res.text)
    # assert res.status_code == 200, "响应状态码非200"
    #
    # assert jsonpath.jsonpath(res.json(),'$.error_code')[0] == 0,'error_code 不等于0'
    client = Client(url="order/",method=METHOD.POST,body_type=BODY_TYPE.FORM)
    client.set_headers({"uid":"4","key":"ab97f63764b608f6d01909d67b4a1c6d"})
    client.set_bodys({"rstr":123,"eid":10})
    client.send()
    client.check_status_code(200)
    client.check_res_times_less_than(1000)
    client.check_json_value('error_code',0)