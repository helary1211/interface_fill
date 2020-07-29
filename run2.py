from core.util import *
import json
from core.client import *
# 1. 读取全局配置  放到全局变量
DATA = get_data_from_sheet('全局变量')
# 2. 接口模板信息
TEMPLATES = get_data_from_sheet('接口模板')
# 3. 拼接好  client对象 拼接请求参数  发送请求 接收响应
cases = get_data_from_sheet('测试用例')

#用例执行的中间信息
infos = []

for index, case in enumerate(cases):
    #开始执行每条测试用例
    if case.get('运行') != 0:
        cid = case.get('用例编号')
        template_name = case.get('模板名称')
        depends = case.get('关联表达式(用例编号=参数路径=临时变量名)')
        params = case.get('参数')
        data = case.get('数据引用')
        checks1 = case.get('响应内容校验1')
        checks2 = case.get('响应内容校验2')
        checks3 = case.get('响应内容校验3')
        status = case.get('响应状态码')
        #校验必填项
        if cid:
            if template_name:
                for T in TEMPLATES:
                    if T.get('接口名称') == template_name:
                        url = T.get('地址')
                        method = T.get('方法类型')
                        body_type = T.get('参数类型')
                        headers = T.get('请求头', '')
                        if url and method and body_type:
                            try:
                                headers = json.loads(headers)
                                #client拼接
                                if body_type == '标准表单':
                                    body_type = 'form'
                                elif body_type == 'JSON':
                                    body_type = 'json'
                                elif body_type == '复合表单':
                                    body_type = 'files'
                                client = Client(url=url, method=method, body_type=body_type)
                                client.set_headers(headers)
                                if params:
                                    try:
                                        params = json.loads(params)
                                        if method == 'POST':
                                            client.set_bodys(params)
                                        elif method == 'GET':
                                            client.params = params

                                        #添加检查点
                                        if status:
                                            client.check_status_code(status)
                                        else:
                                            client.check_status_code_is_200()

                                        if checks1:
                                            checks_list = checks1.split(',')
                                            if checks_list[0] == '时间':
                                                client.check_res_times_less_than(int(checks_list[1]))
                                            elif checks_list[0] == '等于':
                                                client.check_res_equal(checks_list[1])
                                            elif checks_list[0] == '包含':
                                                client.check_res_contains(checks_list[1])
                                            elif checks_list[0] == '节点':
                                                client.check_json_value(checks_list[1], checks_list[2])
                                            else:
                                                print('检查点类型无效')

                                        if checks2:
                                            checks_list = checks1.split(',')
                                            if checks_list[0] == '时间':
                                                client.check_res_times_less_than(int(checks_list[1]))
                                            elif checks_list[0] == '等于':
                                                client.check_res_equal(checks_list[1])
                                            elif checks_list[0] == '包含':
                                                client.check_res_contains(checks_list[1])
                                            elif checks_list[0] == '节点':
                                                client.check_json_value(checks_list[1], checks_list[2])
                                            else:
                                                print('检查点类型无效')

                                        if checks3:
                                            checks_list = checks1.split(',')
                                            if checks_list[0] == '时间':
                                                client.check_res_times_less_than(int(checks_list[1]))
                                            elif checks_list[0] == '等于':
                                                client.check_res_equal(checks_list[1])
                                            elif checks_list[0] == '包含':
                                                client.check_res_contains(checks_list[1])
                                            elif checks_list[0] == '节点':
                                                client.check_json_value(checks_list[1], checks_list[2])
                                            else:
                                                print('检查点类型无效')

                                    except:
                                        infos.append({'id': cid, "result": "skip", "log": ['正文参数格式错误']})
                            except:
                                infos.append({'id': cid, "result": "skip", "log": ['接口模板头信息格式错误']})
                        else:
                            infos.append({'id': cid, "result": "skip", "log": ['接口模板数据错误']})
                        #拼接client对象
                        break
                else:
                    infos.append({'id': cid, "result": "skip", "log": ['引用的接口模板不存在']})
                    continue

            else:
                infos.append({'id': cid, "result": "skip", "log": ['模板名称为空']})
                continue
        else:
            infos.append({'id': '', "result": "skip", "log":['第{index}行测试用例，标号为空'.format(
                index=index
            )]})
            continue
    else:
        continue

