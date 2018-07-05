#coding:utf-8
import requests
import readConfig
from common import configHttp
from common.Log import MyLog as Log
import json
import os
from xlrd import open_workbook
from xml.etree import ElementTree




localReadConfig = readConfig.ReadConfig()
proDir = readConfig.proDir
localConigHttp = configHttp.ConfigHttp()
log = Log.get_log()
logger = log.get_logger()
caseNo = 0

def get_visitor_token():
    host = localReadConfig.get_http("BASEURL")
    response = requests.get(host+"/xlcp/UserBind/testLoginTwo")
    info = response.json()
    token = info.get("info")
    logger.debug("Create token:%s" % (token))
    return token

def set_visitor_token_to_config():
    token_v = get_visitor_token()
    localReadConfig.set_headers("TOKEN_V",token_v)

def get_value_from_return_json_get(json,name1,name2,name3,name4,name):
    info = json["code"]
    if info == 0:
        print("请求返回code值：%s" %info)
        logger.info("请求返回code值：%s" %info)
        print("孩子的验证信息：%s——%s——%s班——%s" %(name1,name2,name3,name4))
        logger.info("孩子的验证信息：%s——%s——%s班——%s" %(name1,name2,name3,name4))
        print('接口数据返回成功，测试用例%s验证成功' % name)
        logger.info('接口数据返回成功，测试用例%s验证成功' % name)
        # print("孩子姓名：",name4)
    else:
        print('error')
    # print('hehehehehehhe')
    # group = json[name1]
    # print(group)
    # value = json[name2]
    # print(value)
    # return info
def get_value_from_return_json_code(json,name):
    print("请求返回code值：%s" %(json['code']))
    logger.info("请求返回code值：%s" %(json['code']))
    print("请求返回data数据：%s" %(json['data']))
    logger.info("请求返回data数据：%s" %(json['data']))
    print("请求返回msg信息：%s" %json['msg'])
    logger.info("请求返回msg信息：%s" %json['msg'])
    if json['code'] != 0:
        print('无接口返回数据，测试用例%s验证成功' % name)
        logger.info('无接口返回数据，测试用例%s验证成功' % name)

def get_value_from_return_json_assertEqual(json,code,msg,name):
    if json['code'] == 0:
        logger.info("code值验证成功:%s" % json['code'])
        print("code值验证成功:%s：" % json['code'])
        logger.info("msg值验证成功：%s" % json['msg'])
        print("msg值验证成功：%s" % json['msg'])
        print('测试用例%s验证成功' % name)
        logger.info('测试用例%s验证成功' % name)
    else:
        print('测试用例%s验证失败，请检查失败原因'% name)
        logger.info('测试用例%s验证失败，请检查失败原因'% name)


def show_return_msg(response):
    url = response.url
    msg = response.text
    print("\n请求地址：" + url)
    logger.info("\n请求地址：" + url)
    # print(msg)
    # 可以显示中文
    print("\n请求返回值：" + '\n' + json.dumps(json.loads(msg), ensure_ascii=False, sort_keys=True, indent=4))
    logger.info("\n请求返回值：" + '\n' + json.dumps(json.loads(msg), ensure_ascii=False, sort_keys=True, indent=4))
    # print(response.headers['Set-Cookie'])

    # print(response.headers)


# ****************************** read testCase excel ********************************

def get_xls(xls_name,sheet_name):
    cls = []
    # 获取xls文件路径
    xlsPath = os.path.join(proDir,"testFile",'case',xls_name)
    # 打开xls文件
    file = open_workbook(xlsPath)
    # 通过名字获取sheel
    sheet = file.sheet_by_name(sheet_name)
    # 获取sheet的行
    nrows = sheet.nrows
    for i in range(nrows):
        if sheet.row_values(i)[0] != u'case_name':
            cls.append(sheet.row_values(i))
    return cls

# ****************************** read SQL xml ********************************
database = {}

def set_xml():
    if len(database) == 0:
        sql_path = os.path.join(proDir,"testFile","SQL.xml")
        tree = ElementTree.parse(sql_path)
        for db in tree.findall("database"):
            db_name = db.get("name")
            table = {}
            for tb in db.getchildren():
                table_name = tb.get("name")
                sql = {}
                for data in tb.getchildren():
                    sql_id = data.get("id")
                    sql[sql_id] = data.text
                table[table_name] = sql
            database[db_name] = table
            logger.info(database[db_name])

    # return  db_name,database[db_name],table[table_name]


def get_xml_dict(database_name, table_name):
    set_xml()
    database_dict = database.get(database_name).get(table_name)
    # print(database_dict)
    return  database_dict

def get_sql(database_name, table_name, sql_id):
    db = get_xml_dict(database_name, table_name)
    sql = db.get(sql_id)
    return sql

# ****************************** read interfaceURL xml ********************************

def get_url_from_xml(name):
    url_list = []
    url_path = os.path.join(proDir, 'testFile', 'interfaceURL.xml')
    tree = ElementTree.parse(url_path)
    for u in tree.findall('url'):
        url_name = u.get('name')
        if url_name == name:
            for c in u.getchildren():
                url_list.append(c.text)
    url = 'http://test2.yuangaofen.com/' + '/'.join(url_list)
   # url = 'http://test3.yuangaofen.com/xlcp/UserBind/testLoginTwo?openid=o96DOt1vjGW2JtWhDw373VvAwjQE'
    return url

if  __name__ == "__main__":
    print(get_xls("login"))
    set_visitor_token_to_config()