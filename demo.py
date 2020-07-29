# _*_ encoding:utf-8 _*_
# @Time : 2020/7/11 14:37
# @Author : chenmeihuan
# @File : demo.py
# @Software: PyCharm
# import jsonpath
# data = {"error_code": 0, "event_list": [
#     {"id": 1, "title": "周末东郊公园户外写生儿童艺术营", "status": 0, "type": "亲子", "price": 450},
#     {"id": 2, "title": "万科翡翠书院•中华礼仪课堂，儿童亲子国学礼仪课", "status": 0, "type": "亲子", "price": 0},
#     {"id": 3, "title": "一起来录广播剧!", "status": 0, "type": "亲子", "price": 209},
#     {"id": 4, "title": "IT高管会战疫系列线上活动", "status": 0, "type": "互联网技术", "price": 0},
#     {"id": 5, "title": "新生·2020 第十二届互联网IT技术主峰会暨金远奖颁奖盛典", "status": 0, "type": "互联网技术", "price": 1000}, {"id": 6, "title": "BOSS俱乐部（北京站）第29期私董会", "status": 0, "type": "创业", "price": 100},
#     {"id": 7, "title": "2020年“赢在苏州·创赢未来”国际IT创客大赛", "status": 0, "type": "创业", "price": 0},
#     {"id": 8, "title": "开心麻花·即兴戏剧Workshop", "status": 0, "type": "文娱", "price": 480},
#     {"id": 9, "title": "面聊口语方庄俱乐部Talking about beauty", "status": 0, "type": "文娱", "price": 50},
#     {"id": 10, "title": "朝圣五台山 户外徒步圣地", "status": 0, "type": "户外", "price": 350},
#     {"id": 11, "title": "端午假期 武功山 云中草原 日出云海 户外天堂 3日穿越活动", "status": 0, "type": "户外", "price": 880}
#     ]
# }
# print(jsonpath.jsonpath(data, '$.error_code'))
# print(jsonpath.jsonpath(data, '$.event_list[0].price'))
# print(data["event_list"][0]["price"])
from xml.etree.cElementTree import *
# import pymysql
# from core.util import *
# host , user, passwd, port, db = get_db_data()
# connect = pymysql.connect(host=host,
#                           user=user,
#                           password=passwd,
#                           port=int(port),
#                           db=db,
#                           charset='utf8')
# cursor = connect.cursor()
# cursor.execute("select user_id from api_userdetail where phone=13800000001")
# result = cursor.fetchall()[0][0]
# print(result)


import xlrd
#打开工作簿workbook
workbook = xlrd.open_workbook('./data/suite.xlsx')
#打开sheet页
sheet = workbook.sheet_by_name('全局变量')
#获取行数  根据行号获取行的内容  根据列号获取列的内容
print(sheet.nrows)
print(sheet.ncols)
print(sheet.row_values(1))
#根据单元格位置获取单元格内容
print(sheet.cell_value(1,1))