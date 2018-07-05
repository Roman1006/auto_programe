#coding:utf-8
import json
import unittest
import requests
import paramunittest
import readConfig as readConfig
from common import Log as Log
from common import common
from common import configHttp as ConfigHttp
from common import configDB as ConfigDB
import time
import urllib
import http.cookiejar
import os
login_xls = common.get_xls("userCase.xlsx", "login")
localReadConfig = readConfig.ReadConfig()
configHttp = ConfigHttp.ConfigHttp()
configDB = ConfigDB.MyDB()
info = {}
cookie_path_p = os.getcwd()
@paramunittest.parametrized(*login_xls)
class Login(unittest.TestCase):
    def setParameters(self,  case_name, method, school_name,student_name, result, code, msg):
        """
        set params
        :param case_name:
        :param method:
        :param token:
        :param email:
        :param password:
        :param result:
        :param code:
        :param msg:
        :return:
        """
        self.case_name = str(case_name)
        self.method = str(method)
        self.school_name = str(school_name)
        self.student_name = str(student_name)
        self.result = str(result)
        self.code = str(code)
        self.msg = str(msg)
        self.return_json = None
        self.info = None
    def description(self):
        """
        test report description
        :return:
        """
        self.case_no
        self.case_name
    def setUp(self):
        """
        :return:
        """
        self.log = Log.MyLog.get_log()
        self.logger = self.log.get_logger()

        print(self.case_name+"测试开始前准备")
        self.logger.info(self.case_name+"测试开始前准备")
    def testLogin(self):
        """
        test body
        :return:
        """
        # set url
        self.url = common.get_url_from_xml('login')
        configHttp.set_url(self.url)
        self.log.build_start_line(self.case_name)
        print("第一步：设置url  "+self.url)
        self.logger.info("第一步：设置url  "+self.url)
        # get visitor token
        # if self.token == '0':
        #     token = localReadConfig.get_headers("token_v")
        # elif self.token == '1':
        #     token = None
        # set headers
        # header = {"token": str(token)}
        # configHttp.set_header(header)
        print("第二步：设置openid")
        self.logger.info("第二步：设置openid")
        sql_openid = common.get_sql("ygf_xlcp_20171208", "user_openid", "openid")
        openid =configDB.executeSQL(sql_openid,(self.student_name,self.school_name))
        # print(openid)
        #
        #
        # print(configHttp.set_header(header))
        # self.logger.info(configHttp.set_header(header))
        # if self.method == 'post':
            # set params
            #data = {"email": self.email, "password": self.password}
            #configHttp.set_data(data)
        if self.method == 'get':
            params = {"openid": openid}
            configHttp.set_params(params)
            print("第三步：设置发送请求的参数")
            self.logger.info("第三步：设置发送请求的参数")
            print(configHttp.set_params(params))
            self.logger.info(configHttp.set_params(params))
            # test interface
            self.return_json = configHttp.get()
        method = str(self.return_json.request)[int(str(self.return_json.request).find('['))+1:int(str(self.return_json.request).find(']'))]
        print("第四步：发送请求\n\t\t请求方式："+method)
        self.logger.info("第四步：发送请求\n\t\t请求方式："+method)
        self.checkResult()

        # check result
    def tearDown(self):
        """

        :return:
        """
        # info = self.info
        # # resultcode
        # if info['code'] == 0:
        #     info1 = info['data']
        #     info2 = info1['stu']
        #     info3 = info2['school']
        #     info4 = info2['grade']
        #     info5 = info2['class_name']
        #     info6 = info2['student_name']
            # get uer token
            # common.get_value_from_return_json_get(info, info3, info4,info5,info6)
            # common.get_value_from_return_json_assertEqual(self.info, self.case_name)
            # set user token to config file
            #localReadConfig.set_headers("TOKEN_U", token_u)
        # else:
        #     pass
        # self.case_name, self.info['resultcode'], self.info['result']
        self.log.build_end_line(self.case_name)
        # self.log.build_case_line(self.case_name, self.info['code'], self.info['msg'])

        print("测试结束，输出log完结\n\n")
        self.logger.info("测试结束，输出log完结\n\n")
    def checkResult(self):
        """
        check test result
        :return:
        """
        self.info = self.return_json.json()
        print("\t\t验证程序返回code值:",self.info['code'])
        if self.info['code'] == 0:
            # print(self.info['data']['stu']['student_no'])
            # 生成cookie文件路径
            # print(cookie_path_p)
            cookie_path = os.path.join(cookie_path_p,"cookie.txt")
            # print(os.path.isfile(cookie_path))
            # 截取cookie值
            cookie_value = str(self.return_json.cookies)[int(str(self.return_json.cookies).find('='))+1:int(str(self.return_json.cookies).find('f'))-1]
            with open(cookie_path,'w')as f:
                f.write(cookie_value)
                print("\t\tcookie值写入成功:",cookie_value)
               # self.logger.info("\t\tcookie值写入成功:",s)
        else:
            print("\t\t不传入cookie值")
            self.logger.info("\t\t不传入cookie值")
        common.show_return_msg(self.return_json)
        print("第五步：检查结果")
        # print(os.path.realpath(__file__))
        # print(os.getcwd())
        self.logger.info("第五步：检查结果")
        info = self.info
        if info['code'] == 0:
            info1 = info['data']
            info2 = info1['stu']
            info3 = info2['school']
            info4 = info2['grade']
            info5 = info2['class_name']
            info6 = info2['student_name']
            common.get_value_from_return_json_get(info, info3, info4, info5, info6,self.case_name)
            self.log.build_sql_line(self.case_name)
            print("开始连接数据库......")
            self.logger.info("开始连接数据库......")
            sql = common.get_sql('ygf_xlcp_20171208', 'user_student_relation', 'select_member')
            cursor_sql_value = configDB.executeSQL(sql, self.student_name)
            print(sql)
            self.logger.info(sql)
            sql_stu_test_code = str(str(self.info['data']['stu']['stu_test_code']))
            with open('E:/XYRGInterface/testCase/user/sql_value.txt','w')as f:
                f.write(sql_stu_test_code)
                print("stu_test_code值写入成功:", sql_stu_test_code)
            print("数据库查询出学生%s学号:%s"%(self.student_name,cursor_sql_value))
            self.logger.info("数据库查询出学生%s学号:%s"%(self.student_name,cursor_sql_value))
            print("接口返回学生%s学号:%s"%(self.student_name,self.info['data']['stu']['student_no']))
            self.logger.info("接口返回学生%s学号:%s"%(self.student_name,self.info['data']['stu']['student_no']))
            self.assertEqual(str(self.info['data']['stu']['student_no']),cursor_sql_value,"学生学号验证不成功")
            if cursor_sql_value == self.info['data']['stu']['student_no']:
                print("学生学号验证成功！！！！")
                configHttp.set_stu_test_code(self.info['data']['stu']['stu_test_code'])
                # print(configHttp.set_stu_test_code(self.info['data']['stu']['stu_test_code']))
                self.logger.info("学生学号验证成功！！！！")
            else:
                print("学生学号验证失败！！！！")
                self.logger.info("学生学号验证失败！！！！")
        else:
            common.get_value_from_return_json_code(info,self.case_name)
        if self.result == '0':
            # email = common.get_value_from_return_json_assertEqual(self.info,self.case_name)
            self.assertEqual(str(self.info['code']), self.code,"code值验证不成功")
            self.assertEqual(str(self.info['msg']), self.msg,"msg信息验证不成功")
        if self.result == '1':
            self.assertEqual(str(self.info['code']), self.code,"code值验证不成功")
            self.assertEqual(str(self.info['msg']), self.msg,"msg信息验证不成功")

