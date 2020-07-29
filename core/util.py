# _*_ encoding:utf-8 _*_
# @Time : 2020/7/12 10:36
# @Author : chenmeihuan
# @File : util.py
# @Software: PyCharm
import csv as CSV
import pytest
import allure
import xml.etree.cElementTree as ET
from data.common_data import *
import xlrd



params = pytest.mark.parametrize
feature = allure.feature
title = allure.title
order = pytest.mark.run


#从外部csv文件，读取参数化数据
def csv(filename):
    result = []
    with open(project_path + '\\data\\'+ filename,'r',encoding='utf-8') as f:
        for i in CSV.reader(f):
            result.append(i)
    return result[1:]

#从外部xml文件读取要运行的测试用例
def get_cases():
    et = ET.ElementTree(file = project_path + '\\config.xml')
    run_cases = []
    for i in et.findall('.//用例集合/*'):
        if i.attrib['run'] == 1:
            run_cases.append('./case/test_{testclass}::test_{testmethod}'.format(testclass=i.split('-')[0],testmethod=i.split('-')[1]))
    return run_cases

#从外部xml文件读取接口配置
def get_interface_conf(name):
    et = ET.ElementTree(file = project_path + '\\config.xml')
    url = ''
    method = ''
    body_type = ''
    for i in et.findall('.//接口模板/' + name + '/*'):
        if i.tag == '地址':
            url = i.text
        elif i.tag == '请求方式':
            method = i.text
        elif i.tag == '正文格式':
            body_type = i.text
    return url, method, body_type

#从外部xml文件读取连接数据的信息
def get_db_data():
    et = ET.ElementTree(file = project_path + '\\config.xml')
    host = ''
    user = ''
    passwd = ''
    port = ''
    db = ''
    for i in et.findall('.//全局配置/MySql/*'):
        if i.tag == 'host':
            host = i.text
        elif i.tag == 'user':
            user = i.text
        elif i.tag == 'passwd':
            passwd = i.text
        elif i.tag == 'db':
            db = i.text
        elif i.tag == 'port':
            port = i.text
    return host, user, passwd, port, db

#从外部xml文件读取全局配置信息
def get_global_info():
    et = ET.ElementTree(file=project_path + '\\config.xml')
    globals = {}
    for i in et.findall('.//全局配置/账号信息/*'):
        globals[i.tag] = i.text
    return globals

#从excel的sheet页获取数据
def get_data_from_sheet(sheet_name):
    data = []

    workbook = xlrd.open_workbook(project_path +'\\data\\suite.xlsx')
    try:
        sheet = workbook.sheet_by_name(sheet_name)
        for i in range(1,sheet.nrows):
            dict={}
            for j in range(0, sheet.ncols):
                dict[sheet.cell_value(0, j)] = sheet.cell_value(i, j)
            data.append(dict)

        return data
    except xlrd.biffh.XLRDError:
        raise Exception('sheet页不存在')


