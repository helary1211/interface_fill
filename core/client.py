# _*_ encoding:utf-8 _*_
# @Time : 2020/7/11 10:30
# @Author : chenmeihuan
# @File : client.py
# @Software: PyCharm
import pymysql
import requests
import jsonpath
import allure
import json
from core.util import *
class Client(object):
    base_url = 'http://123.56.99.53:9000/event/api/'
    def __init__(self, url, method, body_type=None, timeout=3, params=None):
        # self.url = Client.base_url + url              #该行用于pytest模板
        self.url = url                                  #该行用于excel驱动模板
        self.method = method
        self.body_type = body_type
        self.params = params
        self.timeout = timeout
        self.headers = {}
        self.data = {}
        self.res = None


    '''按照key-value键值对的形式一个一个加'''
    def set_header(self, key, value):
        self.headers[key] = value

    '''用data的值替换headers字典'''
    def set_headers(self, data):
        if isinstance(data, dict):
            self.headers = data
        else:
            raise Exception('头信息应以字典形式传递！')

    def set_body(self, key, value):
        self.data[key] = value

    '''用data的值替换datas字典'''
    def set_bodys(self, data):
        if isinstance(data, dict):
            self.data = data
        else:
            raise Exception('头信息应以字典形式传递！')

    '''按照key-value键值对的形式一个一个加'''
    def set_param(self, key, value):
        self.params[key] = value

    '''用data的值替换headers字典'''
    def set_params(self, data):
        if isinstance(data, dict):
            self.params = data
        else:
            raise Exception('头信息应以字典形式传递！')


    '''发送请求'''
    @allure.step('请求接口详细信息')
    def send(self):
        if self.method == 'GET':
            self.res = requests.get(url=self.url, headers=self.headers, params=self.params,
                                    timeout = self.timeout)
        elif self.method == 'POST':
            if self.body_type == 'form':
                self.set_header('Content-Type','application/x-www-form-urlencoded')
                self.res = requests.post(url=self.url, headers=self.headers, params=self.params,
                                         data=self.data, timeout = self.timeout)
            elif self.body_type == 'files':
                self.res = requests.post(url=self.url, headers=self.headers, params=self.params,
                                         files=self.data, timeout = self.timeout)
            elif self.body_type == 'json':
                self.set_header('Content-Type','application/json')
                self.res = requests.post(url=self.url, headers=self.headers, params = self.params,
                                         data=self.data, timeout = self.timeout)
            else:
                raise Exception('请求正文格式错误！')
        allure.attach(self.url,'请求地址',allure.attachment_type.TEXT)
        allure.attach(self.method,'请求地址',allure.attachment_type.TEXT)
        allure.attach(json.dumps(self.headers),'请求头',allure.attachment_type.TEXT)
        allure.attach(json.dumps(self.data),'请求正文',allure.attachment_type.TEXT)
        allure.attach(self.res_text,'响应内容',allure.attachment_type.TEXT)


    '''获取响应状态码'''
    @property
    def status_code(self):
        if self.res is not None:
            return self.res.status_code
        else:
            print("响应内容为空，响应状态码获取失败！")
            return None

    '''获取响应时间'''
    @property
    def res_times(self):
        if self.res is not None:
            return round(self.res.elapsed.total_seconds()*1000)
        else:
            print("获取响应时间失败")
            return None

    '''获取响应内容'''
    @property
    def res_text(self):
        if self.res is not None:
            return self.res.text
        else:
            print("响应内容为空，响应内容获取失败")
            return None

    '''获取cookie'''
    @property
    def cookies(self):
        if self.res is not None:
            return self.res.cookies
        else:
            print("响应内容为空，cookies获取失败")
            return None

    '''将响应内容变成字典格式'''
    def res_to_json(self):
        if self.res is not None:
            return self.res.json()
        else:
            print("响应内容为空，响应内容获取失败")
            return None

    '''获取jsonpath值'''
    def get_json_value(self, express):
        if not express.startswith('$.'):
            express = '$.' + express
        if self.res_to_json() is not None:
            value = jsonpath.jsonpath(self.res_to_json(),express)
            if value:
                return value[0]
            else:
                print("j，没有找到对应值！")
                return None
        else:
            print("响应内容为空，响应内容获取失败")
            return None



    def get_db_data(self,sqlStr):
        host, user, passwd, port, db = get_db_data()
        try:
            connect = pymysql.connect(host=host,
                                      user=user,
                                      password=passwd,
                                      port=int(port),
                                      db=db,
                                      charset='utf8')
            cursor = connect.cursor()
            cursor.execute(sqlStr)
            result = cursor.fetchall()

        except:
            print("连接数据库失败")
        finally:
            connect.close()
        return str(result[0][0])


    @allure.step('检查响应状态码')
    def check_status_code(self, status_code):
        assert self.status_code == status_code, '响应状态码错误！实际结果【{actual}】，预期结果【{expected}】'\
            .format(actual=self.res.status_code, expected=status_code)


    @allure.step('检查响应时间')
    def check_res_times_less_than(self, times):
        assert self.res_times < times, '响应状态码错误！实际结果【{actual}ms】，预期结果【小于{expected}ms】'\
            .format(actual=self.res_times, expected=times)


    @allure.step('检查响应内容相等')
    def check_res_equal(self,expected):
        assert self.res_text == expected, '响应内容不一致！实际结果【{actual}】，预期结果【{expected}】'\
            .format(actual=self.res_text, expected=expected)

    @allure.step('检查响应包含特定字符串')
    def check_res_contains(self, str):
        assert str in self.res_text, '响应内容不包含关键信息！实际结果【{actual}】，关键信息【{expected}】'\
            .format(actual=self.res_text, expected=str)

    @allure.step('检查json节点数据')
    def check_json_value(self,path,expected):
        actual_value = self.get_json_value(path)
        assert str(actual_value) == str(expected), '响应json节点检查失败，实际结果【{actual}】，预期结果【{expected}】，json节点路径【{path}】'\
            .format(actual=actual_value,expected=expected,path=path)

    @allure.step('mysql数据库校验')
    def check_mysql_value(self,sqlStr,jsonPath):
        sqlData = self.get_db_data(sqlStr)
        resData = self.get_json_value(jsonPath)
        assert resData == sqlData, '数据库查询到的结果是：【{sqlData}】,接口返回实际结果是【{resData}】'\
            .format(sqlData=sqlData,resData=resData)

    def check_multi_point(self,check_point):
        check_list = check_point.split(',')
        if check_list[0] == '响应时间':
            self.check_res_times_less_than(int(check_list[1]))
        elif check_list[0] == '响应等于':
            self.check_res_equal(check_list[1])
        elif check_list[0] == '响应包含':
            self.check_res_contains(check_list[1])
        elif check_list[0] == '节点检查':
            self.check_json_value(check_list[1], check_list[2])
        else:
            print("不支持您的检查点类型:" + check_point)

'''定义请求方式'''
class METHOD(object):
    POST = 'POST'
    GET = 'GET'

'''定义请求正文格式'''
class BODY_TYPE(object):
    FORM = 'form'
    FILE = 'files'
    JSON = 'json'



