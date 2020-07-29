# _*_ encoding:utf-8 _*_
# @Time : 2020/7/27 18:10
# @Author : chenmeihuan
# @File : run3.py
# @Software: PyCharm
from core.util import *
import json
from core.client import *
#读取全局配置
DATA = get_data_from_sheet('全局变量1')
#读取接口模板信息
TEMPLATES = get_data_from_sheet('接口模板')
#读取测试用例
cases = get_data_from_sheet('测试用例')
#用例执行的中间信息
infos = []


for index,case in enumerate(cases):
    if case.get('运行') != '0':
        cid = case.get('用例编号')
        template_name = case.get('模板名称')
        depends = case.get('关联表达式（用例编号=参数路径=临时变量）')
        params = case.get('参数')
        data = case.get('数据引用')
        check1 = case.get('响应内容校验1')
        check2 = case.get('响应内容校验2')
        check3 = case.get('响应内容校验3')
        status = case.get('响应状态码')
        run_flag = True
        #校验excel必填项
        if cid:
            if template_name:
                for T in TEMPLATES:
                    if T.get('接口名称') == template_name:
                        url = T.get('地址')
                        method = T.get('方法类型')
                        body_type = T.get('参数类型')
                        headers = T.get('请求头')
                        #找到url、method、body_type后开始拼接client
                        if url and method and body_type:
                                if body_type == '标准表单':
                                    body_type = 'form'
                                elif body_type == 'JSON':
                                    body_type = 'json'
                                elif body_type == '复合表单':
                                    body_type = 'files'
                                client = Client(url=DATA[0]['base_url'] + url, method=method, body_type=body_type)

                        else:
                            infos.append({'id': cid, 'result': 'skip', 'log': ['接口模板数据错误']})
                            continue

                        #判断头信息
                        if headers:
                            try:
                                headers = json.loads(headers)
                                client.set_headers(headers)
                            except:
                                infos.append({'id': cid, 'result': 'skip', 'log': ['接口模板头信息错误']})
                                continue
                        else:
                            headers = {}

                        #判断接口参数
                        if params:
                            try:
                                params = json.loads(params)
                                if method == 'POST':
                                    client.set_bodys(params)
                                elif method == 'GET':
                                    client.params = params
                            except:
                                infos.append({'id': cid, 'result': 'skip', 'log': ['接口正文参数异常']})
                                continue

                        #发送请求
                        client.send()

                        #添加检查点
                        if status:
                            try:
                                client.check_status_code(int(status))
                            except:
                                infos.append({'id':cid, 'result':'fail','log':['响应状态码校验失败']})
                                run_flag = False

                        if check1:
                            try:
                                client.check_multi_point(check1)
                            except:
                                run_flag = False
                                infos.append({'id':cid, 'result':'fail','log':['{check}:校验失败'.format(check=check1)]})

                        if check2:
                            try:
                                client.check_multi_point(check2)
                            except:
                                run_flag = False
                                infos.append({'id': cid, 'result': 'fail', 'log': ['{check}:校验失败'.format(check=check2)]})

                        if check3:
                            try:
                                client.check_multi_point(check3)
                            except:
                                run_flag = False
                                infos.append({'id': cid, 'result': 'fail', 'log': ['{check}:校验失败'.format(check=check3)]})

                        if run_flag:
                            infos.append({'id':cid, 'result':'success', 'log':['该用例运行成功']})
                        break
                    else:
                        infos.append({'id':cid, 'result':'skip', 'log':['{template}接口模板不存在'.format(template=template_name)]})
            else:
                infos.append({"id": cid, "result": "skip", "log": ['模板名称为空']})
        else:
            infos.append({"id":"", "result":"skip", "log":['第{index}行测试用例，编号为空！'.format(index = index)]})
    else:
        continue

print(infos)