#coding:utf-8
import json
import unittest
import paramunittest
import readConfig as readConfig
from common import Log as Log
from common import common
from common import configHttp as ConfigHttp
from common import configDB as ConfigDB
from decimal import  Decimal
import os

login_xls = common.get_xls("userCase.xlsx", "zhonghe")
localReadConfig = readConfig.ReadConfig()
configHttp = ConfigHttp.ConfigHttp()
configDB = ConfigDB.MyDB()
info = {}
cookie_v = []
# 获取当前文件目录
proDir = os.path.split(os.path.realpath(__file__))[0]
@paramunittest.parametrized(*login_xls)
class Login(unittest.TestCase):
    def setParameters(self, case_name, method, token, type, student_name, result, code, msg):
        """
        set params
        :param case_name:
        :param method:
        :param token:
        :param JSESSIONID:
        :param type:
        :param result:
        :param code:
        :param msg:
        :return:
        """
        self.case_name = str(case_name)
        self.method = str(method)
        self.token = str(token)
        # self.JSESSIONID = str(JSESSIONID)
        self.type = str(type)
        self.student_name = str(student_name)
        self.result = str(result)
        self.code = int(code)
        self.msg = str(msg)
        self.return_json = None
        self.info = None
    def description(self):
        """
        test report description
        :return:
        """
        self.case_name
    def setUp(self):
        """
        :return:
        """
        self.log = Log.MyLog.get_log()
        self.logger = self.log.get_logger()
        cookie_path = os.path.join(proDir,"cookie.txt")
        with open(cookie_path,'r') as f:
            cookie_value = f.readline()
            cookie_v.append(cookie_value)
        print(self.case_name+"测试开始前准备")
        self.logger.info(self.case_name + "测试开始前准备")
    def testLogin(self):
        """
        test body
        :return:
        """
        # set url
        self.url = common.get_url_from_xml('zhonghe')
        configHttp.set_url(self.url)
        print("第一步：设置url  "+self.url)
        self.logger.info("第一步：设置url  " + self.url)
        # get visitor token
        # if self.token == '0':
        #     token = localReadConfig.get_headers("token_v")
        # elif self.token == '1':
        #     token = None
        #
        # set headers
        # header = {"JSESSIONID": str(token)}
        # configHttp.set_header(header)
        print("第二步：设置cookie")
        self.logger.info("第二步：设置cookie")
        cookie = {"JSESSIONID": cookie_v[0]}
        configHttp.set_cookies(cookie)
        print(configHttp.set_cookies(cookie))
        self.logger.info(configHttp.set_cookies(cookie))
        # set params
        print("第三步：设置发送请求的参数")
        self.logger.info("第三步：设置发送请求的参数")
        data = {"type": self.type, "JSESSIONID": cookie_v[0]}
        print(configHttp.set_data(data))
        self.logger.info(configHttp.set_data(data))
        # test interface
        self.return_json = configHttp.postWriteJson()
        # self.return_json.encoding = "UTF-8"
        # print(self.return_json.url)

        method = str(self.return_json.request)[int(str(self.return_json.request).find('['))+1:int(str(self.return_json.request).find(']'))]
        print("第四步：发送请求\n\t\t请求方法："+method)
        self.logger.info("第四步：发送请求\n\t\t请求方法："+method)

        # check result
        self.checkResult()
        print("第五步：检查结果")
        self.logger.info("第五步：检查结果")
    def tearDown(self):
        """

        :return:
        """
        self.log.build_end_line(self.case_name)
        print("测试结束，输出log完结\n\n")
        self.logger.info("测试结束，输出log完结\n\n")
    def executeSQL(self,testid,stem_no,quest_id):


        cand_no_path = os.path.join(proDir,"sql_value.txt")
        with open(cand_no_path, 'r') as f:
            sql_value = f.readline()
        sql_testid = common.get_sql('ygf_xlcp_20171208', 'user', 'test_id')
        cursor_sql_value_testid = configDB.executeSQL_all(sql_testid, (self.student_name, sql_value))
        sql_zong_avgscore = common.get_sql('ygf_xlcp_20171208', 'answer', 'avgscore')
        V_zong_avgscore = configDB.executeSQL_all(sql_zong_avgscore, (testid, sql_value, quest_id, stem_no))
        a = "".join(V_zong_avgscore)
        v_zpzong_avgscore = float(a[int(a.find('(') + 2):int(a.find(')') - 1)])
        sql_history_avg = common.get_sql('ygf_xlcp_20171208', 'quest_history_info', 'history_avg')
        V_history_avg = configDB.executeSQL_all(sql_history_avg, quest_id)
        b = "".join(V_history_avg)
        len_b = len(b)
        history_avg = float(b[(int(b.find('.') - 1)):int(b.find(','))])
        history_standard_deviation = float(b[(int(b.find(',') + 2)):len_b])
        v_zp_zf = (v_zpzong_avgscore - history_avg) / history_standard_deviation
        dic_zp_zf = Decimal(v_zp_zf)
        dic_zp_zf = round(dic_zp_zf, 2)
        sql_zp_bfs = common.get_sql('ygf_xlcp_20171208', 'standard_normal_info', 'results_value')
        V_zp_bfs = configDB.executeSQL_all(sql_zp_bfs, dic_zp_zf)
        v_zp_bfs = float("".join(V_zp_bfs))
        v_zp_zhpf = (v_zp_bfs * 60) + 35
        v_zp_cufen = v_zpzong_avgscore * 20
        dic_v_zp_cufen = Decimal(v_zp_cufen)
        dic_v_zp_cufen = round(dic_v_zp_cufen, 3)
        if quest_id == 20:
            print("**************** A-JS ****************")
            print("学生日常行为量表（A-JS） quest_id:%s 学生:%s" % (quest_id, self.student_name))
            print('查询个人总维度平均分sql语句：', sql_zong_avgscore)
            print('查询量表总维度平均分sql语句：', sql_history_avg)
            print('个人总维度平均分：', v_zpzong_avgscore)
            print('自评总体百分位数：', v_zp_bfs)
            print('自评总粗分：', dic_v_zp_cufen)
            print('自评个人总Z分：', v_zp_zf)
            print('自评个人总评分', v_zp_zhpf)
            print('全局总维度平均分：', history_avg)
            print('全局标准差：', history_standard_deviation)

            ziping_data = self.info['data'][0]
            ziping = ziping_data['ziping']
            zp_avg = ziping['zp_avg']
            zp_bfs = ziping['zp_bfs']
            zp_cufen = ziping['zp_cufen']
            zp_zhpf = ziping['zp_zhpf']
            zp_zf = ziping['zp_zf']
            dic_zp_cufen = Decimal(zp_cufen)
            dic_zp_cufen = round(dic_zp_cufen, 3)

            self.assertEqual(zp_avg, v_zpzong_avgscore, '自评个人总维度平均分zp_avg校验失败')
            self.assertEqual(zp_bfs, v_zp_bfs, '自评总体百分位数zp_bfs校验失败')
            self.assertEqual(dic_zp_cufen, dic_v_zp_cufen, '自评总粗分zp_cufen校验失败')
            self.assertEqual(zp_zf, v_zp_zf, '自评个人总Z分数zp_zf校验失败')
            self.assertEqual(zp_zhpf, v_zp_zhpf, '自评总评分zp_zhpf校验失败')

            if zp_avg == v_zpzong_avgscore:
                print("自评个人总平均分zp_avg验证成功！")
            else:
                print("自评个人总平均分zp_avg验证失败！")
            if zp_bfs == v_zp_bfs:
                print('自评总体百分位数zp_bfs验证成功！')
            else:
                print('自评总体百分位数zp_bfs验证失败！')
            if dic_zp_cufen == dic_v_zp_cufen:
                print('自评总粗分zp_cufen验证成功！')
            else:
                print('自评总粗分zp_cufen验证失败！')
            if zp_zf == v_zp_zf:
                print('自评个人总Z分数zp_zf验证成功！')
            else:
                print('自评个人总Z分数zp_zf验证失败！')

            if zp_zhpf == v_zp_zhpf:
                print('自评总评分zp_zhpf验证成功！')
            else:
                print('自评总评分zp_zhpf验证失败！')
        if quest_id ==25:
            print("**************** H-JS ****************")
            print("初中生日常行为家长评定量表（H-JS） quest_id:%s 学生:%s" % (quest_id, self.student_name))
            print('查询个人总维度平均分sql语句：', sql_zong_avgscore)
            print('查询量表总维度平均分sql语句：', sql_history_avg)
            print('个人总维度平均分：', v_zpzong_avgscore)
            print('他评总体百分位数：', v_zp_bfs)
            print('他评总粗分：', dic_v_zp_cufen)
            print('他评个人总Z分：', v_zp_zf)
            print('他评个人总评分', v_zp_zhpf)
            print('他评全局总维度平均分：', history_avg)
            print('他评全局标准差：', history_standard_deviation)

            taping_data = self.info['data'][1]
            taping = taping_data['taping']
            tp_avg = taping['tp_avg']
            tp_bfs = taping['tp_bfs']
            tp_cufen = taping['tp_cufen']
            tp_zhpf = taping['tp_zhpf']
            tp_zf = taping['tp_zf']
            dic_tp_cufen = Decimal(tp_cufen)
            dic_tp_cufen = round(dic_tp_cufen, 3)

            self.assertEqual(tp_avg, v_zpzong_avgscore, '他评个人总维度平均分tp_avg校验失败')
            self.assertEqual(tp_bfs, v_zp_bfs, '他评总体百分位数tp_bfs校验失败')
            self.assertEqual(dic_tp_cufen, dic_v_zp_cufen, '他评总粗分tp_cufen校验失败')
            self.assertEqual(tp_zf, v_zp_zf, '他评个人总Z分数tp_zf校验失败')
            self.assertEqual(tp_zhpf, v_zp_zhpf, '他评总评分tp_zhpf校验失败')

            if tp_avg == v_zpzong_avgscore:
                print("他评个人总平均分zp_avg验证成功！")
            else:
                print("他评个人总平均分zp_avg验证失败！")
            if tp_bfs == v_zp_bfs:
                print('他评总体百分位数zp_bfs验证成功！')
            else:
                print('他评总体百分位数zp_bfs验证失败！')
            if dic_tp_cufen == dic_v_zp_cufen:
                print('他评总粗分zp_cufen验证成功！')
            else:
                print('他评总粗分zp_cufen验证失败！')
            if tp_zf == v_zp_zf:
                print('他评个人总Z分数zp_zf验证成功！')
            else:
                print('他评个人总Z分数zp_zf验证失败！')

            if tp_zhpf == v_zp_zhpf:
                print('他评总评分zp_zhpf验证成功！')
            else:
                print('他评总评分zp_zhpf验证失败！')
        if quest_id == 22:
            print("**************** C-JS ****************")
            print("初中家长教育行为学生感知量表（C - JS） quest_id:%s 学生:%s" % (quest_id, self.student_name))
            print('查询个人总维度平均分sql语句：', sql_zong_avgscore)
            print('查询量表总维度平均分sql语句：', sql_history_avg)
            print('个人总维度平均分：', v_zpzong_avgscore)
            print('他评总体百分位数：', v_zp_bfs)
            print('他评总粗分：', dic_v_zp_cufen)
            print('他评个人总Z分：', v_zp_zf)
            print('他评个人总评分', v_zp_zhpf)
            print('他评全局总维度平均分：', history_avg)
            print('他评全局标准差：', history_standard_deviation)

            taping_data = self.info['data'][1]
            taping = taping_data['taping']
            tp_avg = taping['tp_avg']
            tp_bfs = taping['tp_bfs']
            tp_cufen = taping['tp_cufen']
            tp_zhpf = taping['tp_zhpf']
            tp_zf = taping['tp_zf']
            dic_tp_cufen = Decimal(tp_cufen)
            dic_tp_cufen = round(dic_tp_cufen, 3)

            self.assertEqual(tp_avg, v_zpzong_avgscore, '他评个人总维度平均分tp_avg校验失败')
            self.assertEqual(tp_bfs, v_zp_bfs, '他评总体百分位数tp_bfs校验失败')
            self.assertEqual(dic_tp_cufen, dic_v_zp_cufen, '他评总粗分tp_cufen校验失败')
            self.assertEqual(tp_zf, v_zp_zf, '他评个人总Z分数tp_zf校验失败')
            self.assertEqual(tp_zhpf, v_zp_zhpf, '他评总评分tp_zhpf校验失败')

            if tp_avg == v_zpzong_avgscore:
                print("他评个人总平均分zp_avg验证成功！")
            else:
                print("他评个人总平均分zp_avg验证失败！")
            if tp_bfs == v_zp_bfs:
                print('他评总体百分位数zp_bfs验证成功！')
            else:
                print('他评总体百分位数zp_bfs验证失败！')
            if dic_tp_cufen == dic_v_zp_cufen:
                print('他评总粗分zp_cufen验证成功！')
            else:
                print('他评总粗分zp_cufen验证失败！')
            if tp_zf == v_zp_zf:
                print('他评个人总Z分数zp_zf验证成功！')
            else:
                print('他评个人总Z分数zp_zf验证失败！')

            if tp_zhpf == v_zp_zhpf:
                print('他评总评分zp_zhpf验证成功！')
            else:
                print('他评总评分zp_zhpf验证失败！')
        if quest_id == 23:
            print("**************** F-JS ****************")
            print("初中家长教育行为量表（F - JS） quest_id:%s 学生:%s" % (quest_id, self.student_name))
            print('查询个人总维度平均分sql语句：', sql_zong_avgscore)
            print('查询量表总维度平均分sql语句：', sql_history_avg)
            print('个人总维度平均分：', v_zpzong_avgscore)
            print('自评总体百分位数：', v_zp_bfs)
            print('自评总粗分：', dic_v_zp_cufen)
            print('自评个人总Z分：', v_zp_zf)
            print('自评个人总评分', v_zp_zhpf)
            print('全局总维度平均分：', history_avg)
            print('全局标准差：', history_standard_deviation)

            ziping_data = self.info['data'][0]
            ziping = ziping_data['ziping']
            zp_avg = ziping['zp_avg']
            zp_bfs = ziping['zp_bfs']
            zp_cufen = ziping['zp_cufen']
            zp_zhpf = round(ziping['zp_zhpf'],2)
            zp_zf = ziping['zp_zf']
            dic_zp_cufen = Decimal(zp_cufen)
            dic_zp_cufen = round(dic_zp_cufen, 3)

            self.assertEqual(zp_avg, v_zpzong_avgscore, '自评个人总维度平均分zp_avg校验失败')
            self.assertEqual(zp_bfs, v_zp_bfs, '自评总体百分位数zp_bfs校验失败')
            self.assertEqual(dic_zp_cufen, dic_v_zp_cufen, '自评总粗分zp_cufen校验失败')
            self.assertEqual(zp_zf, v_zp_zf, '自评个人总Z分数zp_zf校验失败')
            self.assertEqual(zp_zhpf, v_zp_zhpf, '自评总评分zp_zhpf校验失败')

            if zp_avg == v_zpzong_avgscore:
                print("自评个人总平均分zp_avg验证成功！")
            else:
                print("自评个人总平均分zp_avg验证失败！")
            if zp_bfs == v_zp_bfs:
                print('自评总体百分位数zp_bfs验证成功！')
            else:
                print('自评总体百分位数zp_bfs验证失败！')
            if dic_zp_cufen == dic_v_zp_cufen:
                print('自评总粗分zp_cufen验证成功！')
            else:
                print('自评总粗分zp_cufen验证失败！')
            if zp_zf == v_zp_zf:
                print('自评个人总Z分数zp_zf验证成功！')
            else:
                print('自评个人总Z分数zp_zf验证失败！')

            if zp_zhpf == v_zp_zhpf:
                print('自评总评分zp_zhpf验证成功！')
            else:
                print('自评总评分zp_zhpf验证失败！')
    def checkResult(self):
        """
        check test result
        :return:
        """
        self.info = self.return_json.json()
        # show return message
        common.show_return_msg(self.return_json)
        if self.info['code'] == 0:
            self.log.build_sql_line(self.case_name)
            with open('E:/XYRGInterface/testCase/user/sql_value.txt', 'r') as f:
                sql_value = f.readline()
            print("开始连接数据库......")
            self.logger.info("开始连接数据库......")

            sql_testid = common.get_sql('ygf_xlcp_20171208', 'user', 'test_id')
            cursor_sql_value_testid = configDB.executeSQL_all(sql_testid, (self.student_name,sql_value))
            number = len(cursor_sql_value_testid)
            if self.type == '学生':
                for i in range(number):
                    testid = cursor_sql_value_testid[i]
                    if testid =='623':
                        stem_no = 63
                        quest_id = 20
                        self.executeSQL(testid,stem_no,quest_id)
                    if testid == '523':
                        stem_no = 63
                        quest_id = 25
                        self.executeSQL(testid,stem_no,quest_id)
            if self.type == '家长':
                for i in range(number):
                    testid = cursor_sql_value_testid[i]
                    if testid =='624':
                        stem_no = 47
                        quest_id = 22
                        self.executeSQL(testid,stem_no,quest_id)
                    if testid == '524':
                        stem_no = 47
                        quest_id = 23
                        self.executeSQL(testid,stem_no,quest_id)
                # with open('E:/XYRGInterface/testCase/user/test_id.txt', 'w')as f:
                #     str = ''
                #     # print(cursor_sql_value_testid)
                #     number = len(cursor_sql_value_testid)
                #     for i in range(number):
                #        str +=cursor_sql_value_testid[i]+' '
                #     f.writelines(str)
            # else:
            #     return 0
            # print(54968453156841324896132129681325)
            # print(sql_testid)
            # self.logger.info(sql_testid)
        if self.result == '0':
            common.get_value_from_return_json_assertEqual(self.info, 'code', 'msg',self.case_name)
            self.assertEqual(self.info['code'], self.code,"code值验证不成功")
            self.assertEqual(self.info['msg'], self.msg,"msg值验证不成功")
        if self.result == '1':
            self.assertEqual(self.info['code'], self.code,"code值验证不成功")
            self.assertEqual(self.info['msg'], self.msg,"msg值验证不成功")
