# _*_ encoding:utf-8 _*_
# @Time : 2020/7/5 15:46
# @Author : chenmeihuan
# @File : conftest.py
# @Software: PyCharm
import pytest
from core.client import *
from core.util import *
import pymysql
# DATA = {"total":0,"success":0,"fail":0,"error":0}
COUNT = {}
GLOBALS = get_global_info()
@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item,call):
    result = yield
    data = result.get_result()
    # if data.when == 'call':
    #     DATA['total'] += 1
    #     if data.outcome == 'passed':
    #         DATA['success'] += 1
    #     elif data.outcome == 'failed':
    #         DATA['fail'] += 1

    if data.when == 'call':
        case_name = data.nodeid
        if case_name != None:
            COUNT[case_name] = data.outcome

#利用工厂夹具函数实现在调用fixture的时候传参
# @pytest.fixture
# def client():
#     def __client(name):
#         url,method,body_type = get_interface_conf(name)
#         cli = Client(url=url, method=method, body_type= body_type)
#         return cli
#     return __client


#利用fixture的反省特性，在运行用例的时候获取用例属性（测试用例方法名，用例所属模块名）
@pytest.fixture
def client(request):
    url, method, body_type = get_interface_conf(request.module.__name__.split('.')[1][5:])
    cli = Client(url=url, method=method, body_type=body_type)
    return cli

#连接数据库
@pytest.fixture(scope='session')
def depends():
    pass

#从xml全局配置取数据
@pytest.fixture
def get():
    def __get(key):
        return GLOBALS[key]
    return __get

#往全局数据GLOBALS大字典里面放值,解决接口的关联问题
@pytest.fixture
def set():
    def __set(key,value):
        GLOBALS[key] = value
    return __set

#解决接口间数据依赖，B接口请求依赖A接口的响应数据
@pytest.fixture
def depends():
    def __depends(module_name, paramsData, json_path):
        url, method, body_type = get_interface_conf(module_name)
        if "params" in paramsData.keys():
            client = Client(url=url, method=method, body_type=body_type, params=paramsData['params'])
        else:
            client = Client(url=url, method=method, body_type=body_type)

        if "headers" in paramsData.keys():
            client.set_headers(paramsData['headers'])
        elif "body" in paramsData.keys():
            client.set_bodys(paramsData['body'])

        client.send()

        return client.get_json_value(json_path)
    return __depends




