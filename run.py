# _*_ encoding:utf-8 _*_
# @Time : 2020/7/5 10:05
# @Author : chenmeihuan
# @File : run.py
# @Software: PyCharm
import pytest
import subprocess
import datetime
import time
from dingtalkchatbot.chatbot import DingtalkChatbot
from cases.conftest import *
from core.util import *
if __name__ == '__main__':
    # pytest.main(['./cases/test_login.py','./cases/test_geteventlist.py','-s'])
    '''运行测试用例'''
    tmp = time.strftime('%Y%m%d_%H%M%S', time.localtime(time.time()))
    run_cmd = get_cases()
    run_cmd.append('-s')
    run_cmd.append('--alluredir=./report/json')
    run_cmd.append('--clean-alluredir')
    run_cmd.append('--reruns=3')
    print(run_cmd)
    pytest.main(run_cmd)
    # pytest.main(['./cases', '-s', '--alluredir=./report/json','--clean-alluredir'])


    '''通过钉钉发送测试结果'''
    total = len(COUNT.keys())
    success = 0
    fail = 0
    for value in COUNT.values():
        if value == 'passed':
            success +=1
        elif value == 'failed':
            fail +=1

    webhook = 'https://oapi.dingtalk.com/robot/send?access_token=aeebc31ea1253fe988ad1c861a7d79fa4309fb6c92aee32a8533a5bfd6305efd'
    xiaoding = DingtalkChatbot(webhook)
    xiaoding.send_text(msg='接口监控测试报告：执行{}，成功{}，失败{}'
                       .format(str(total),str(success),str(fail)),
                       at_mobiles=['15311449802'])
    # xiaoding.send_image(pic_url='https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1593942408605&di=98a170aa66bc1156e4f768bb75dc5efb&imgtype=0&src=http%3A%2F%2Fimg.pconline.com.cn%2Fimages%2Fupload%2Fupc%2Ftx%2Fwallpaper%2F1304%2F17%2Fc5%2F19955421_1366189671581.jpg')
    # xiaoding.send_text(msg='接口监控测试结果：')

    '''通过allure生成测试报告'''
    time_stamp = '{0:%Y%m%d_%H%M%S}'.format(datetime.datetime.now())
    result_path = './report/html/' + time_stamp
    cmd = 'allure generate ./report/json -o ' + result_path
    subprocess.call(cmd, shell=True)