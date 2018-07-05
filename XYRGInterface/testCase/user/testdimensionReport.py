#coding:gbk
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

login_xls = common.get_xls("userCase.xlsx", "weidu")
localReadConfig = readConfig.ReadConfig()
configHttp = ConfigHttp.ConfigHttp()
configDB = ConfigDB.MyDB()
info = {}
cookie_v = []
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
        self.type = str(type)
        self.student_name = str(student_name)
        self.result = str(result)
        self.code = int(code)
        self.msg = str(msg)
        self.return_json = None
        self.info = None
        self.zp_zf = None
        self.tp_zf = None
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
        cookie_path = os.path.join(proDir, "cookie.txt")
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
        self.url = common.get_url_from_xml('weidu')
        configHttp.set_url(self.url)
        print("第一步：设置url  "+self.url)
        self.logger.info("第一步：设置url  " + self.url)
        print("第二步：设置cookie")
        self.logger.info("第二步：设置cookie")
        cookie = {"JSESSIONID": cookie_v[0]}
        configHttp.set_cookies(cookie)
        print(configHttp.set_cookies(cookie))
        self.logger.info(configHttp.set_cookies(cookie))
        print("第三步：设置发送请求的参数")
        self.logger.info("第三步：设置发送请求的参数")
        data = {"type": self.type, "JSESSIONID": cookie_v[0]}
        print(configHttp.set_data(data))
        self.logger.info(configHttp.set_data(data))
        self.return_json = configHttp.postWriteJson()
        method = str(self.return_json.request)[int(str(self.return_json.request).find('['))+1:int(str(self.return_json.request).find(']'))]
        print("第四步：发送请求\n\t\t请求方法："+method)
        self.logger.info("第四步：发送请求\n\t\t请求方法："+method)
        self.checkResult()
        print("第五步：检查结果")
        self.logger.info("第五步：检查结果")
    # 程序返回的自评相关数据
    def cx_weidu_value(self,data_value,number,vd_name,quest_id):
        cx_zp_value = []
        cx_tp_value = []
        if quest_id == 20 or quest_id == 23:
            zp_value = data_value[number]['dim_zp_info']
            zp_baifenlv = round(zp_value['zh_baifenlv'], 2)
            zp_bfs = round(zp_value['zp_bfs'], 2)
            zp_cufen = round(zp_value['zp_cufen'], 2)
            zp_zf = round(zp_value['zp_zf'], 2)
            zp_zhpf = round(zp_value['zp_zhpf'], 2)
            print("----------程序返回%s自评相关数据----------" % vd_name)
            print("程序返回%szp_baifenlv:%s" % (vd_name, zp_baifenlv))
            cx_zp_value.append(zp_baifenlv)
            print("程序返回%szp_bfs:%s" % (vd_name, zp_bfs))
            cx_zp_value.append(zp_bfs)
            print("程序返回%szp_cufen:%s" % (vd_name, zp_cufen))
            cx_zp_value.append(zp_cufen)
            print("程序返回%szp_zf:%s" % (vd_name, zp_zf))
            cx_zp_value.append(zp_zf)
            print("程序返回%szp_zhpf:%s" % (vd_name, zp_zhpf))
            cx_zp_value.append(zp_zhpf)
            return cx_zp_value
        if quest_id == 25 or quest_id == 22:
            tp_value = data_value[number]['dim_tp_info']
            tp_baifenlv = round(tp_value['th_baifenlv'], 2)
            tp_bfs = round(tp_value['tp_bfs'], 2)
            tp_cufen = round(tp_value['tp_cufen'], 2)
            tp_zf = round(tp_value['tp_zf'], 2)
            tp_zhpf = round(tp_value['tp_zhpf'], 2)
            print("----------程序返回%s自评相关数据----------" % vd_name)
            print("程序返回%stp_baifenlv:%s" % (vd_name, tp_baifenlv))
            cx_tp_value.append(tp_baifenlv)
            print("程序返回%stp_bfs:%s" % (vd_name, tp_bfs))
            cx_tp_value.append(tp_bfs)
            print("程序返回%stp_cufen:%s" % (vd_name, tp_cufen))
            cx_tp_value.append(tp_cufen)
            print("程序返回%stp_zf:%s" % (vd_name, tp_zf))
            cx_tp_value.append(tp_zf)
            print("程序返回%stp_zhpf:%s" % (vd_name, tp_zhpf))
            cx_tp_value.append(tp_zhpf)
            return cx_tp_value
    # 计算全局相关数据【各维度平均分和方差】
    def qj_sql_value(self,quest_id,wu_name,avg_value):
        # 查询全局维度分
        sql_dim_jq_info = common.get_sql('ygf_xlcp_20171208', 'quest_history_info_dimension', 'dimension_info')
        dimension_info = configDB.executeSQL(sql_dim_jq_info, quest_id)
        # [{'维度名': '自主学习意识', '平均分': '3.7802', '标准差': '0.7009'},
        # {'维度名': '自主学习情绪', '平均分': '3.4144', '标准差': '0.76397'},
        # {'维度名': '自主学习倾向', '平均分': '3.0944', '标准差': '0.62917'},
        # {'维度名': '自主学习效能感', '平均分': '3.2014', '标准差': '0.79273'},
        # {'维度名': '自主学习习惯', '平均分': '3.2221', '标准差': '0.75463'},
        # {'维度名': '学习环境控制', '平均分': '3.1834', '标准差': '0.80796'}]
        # 计算个维度百分位数
        # 将列表形式的str转化为list
        dimension_info = eval(dimension_info)  # <class 'list'>
        dim_info_len = len(dimension_info)  # 6
        for i in range(dim_info_len):
            dic_num = len(dimension_info[i])   # 3
            list_values = dimension_info[i]  #<class 'dict'>
            if list_values['维度名'] == wu_name:
                vd_avg = float('%.4f' % (float(list_values['平均分'])))
                vd_bzc = float('%.4f' % (float(list_values['标准差'])))
                vd_zp_zf = round((float(avg_value) - vd_avg) / vd_bzc, 2)
                print("----------数据库查询%s全局相关数据----------" % wu_name)
                print("查询出%s全局平均分:%s" % (wu_name, vd_avg))
                print("查询出%s全局标准差:%s" % (wu_name, vd_bzc))
                if quest_id == 20 or quest_id == 23:
                    self.zp_zf = vd_zp_zf
                if quest_id == 25 or quest_id == 22:
                    self.tp_zf = vd_zp_zf
    # 根据数据库查询结果计算维度自评相关数据
    def sql_weidu_value(self,wd_name,sql_zp_bfs,wd_zp_zf,avg_value,quest_id):
        sql_zp_value = []
        sql_tp_value = []
        if quest_id ==20 or quest_id == 23:
            V_zp_bfs = configDB.executeSQL_all(sql_zp_bfs, wd_zp_zf)
            v_zp_bfs = float("".join(V_zp_bfs))
            v_zp_zhpf = round((v_zp_bfs * 60) + 35,2)
            v_zp_cufen = round(avg_value * 20,2)
            v_zh_baifenlv = round(100 - v_zp_zhpf,2)
            print("----------根据数据库数据计算出%s自评相关数据----------" % wd_name)
            print("计算出%s个人平均分:%s" % (wd_name, avg_value))
            # sql_zp_value.append(float(avg_value))
            print("计算出%szh_baifenlv:%s" % (wd_name, v_zh_baifenlv))
            sql_zp_value.append(v_zh_baifenlv)
            print("计算出%szp_bfs：%s" % (wd_name, v_zp_bfs))
            sql_zp_value.append(v_zp_bfs)
            print("计算出%szp_cufen:%s" % (wd_name, v_zp_cufen))
            sql_zp_value.append(float(v_zp_cufen))
            print("计算出%sZ分数:%s" % (wd_name, wd_zp_zf))
            sql_zp_value.append(wd_zp_zf)
            print("计算出%szp_zhpf：%s" % (wd_name, v_zp_zhpf))
            sql_zp_value.append(v_zp_zhpf)
            return sql_zp_value
        if quest_id == 25 or quest_id == 22:
            V_tp_bfs = configDB.executeSQL_all(sql_zp_bfs, wd_zp_zf)
            v_tp_bfs = float("".join(V_tp_bfs))
            v_tp_zhpf = round((v_tp_bfs * 60) + 35,2)
            v_tp_cufen = round(avg_value * 20,2)
            v_th_baifenlv = round(100 - v_tp_zhpf,2)
            print("----------根据数据库数据计算出%s他评相关数据----------" % wd_name)
            print("计算出%s个人平均分:%s" % (wd_name, avg_value))
            # sql_tp_value.append(float(avg_value))
            print("计算出%sth_baifenlv:%s" % (wd_name, v_th_baifenlv))
            sql_tp_value.append(v_th_baifenlv)
            print("计算出%stp_bfs：%s" % (wd_name, v_tp_bfs))
            sql_tp_value.append(v_tp_bfs)
            print("计算出%stp_cufen:%s" % (wd_name, v_tp_cufen))
            sql_tp_value.append(float(v_tp_cufen))
            print("计算出%sZ分数:%s" % (wd_name, wd_zp_zf))
            sql_tp_value.append(wd_zp_zf)
            print("计算出%stp_zhpf：%s" % (wd_name, v_tp_zhpf))
            sql_tp_value.append(v_tp_zhpf)
            return sql_tp_value
    def value_asser(self,value1,value2):
        if (len(value1) == len(value2)):
            for num in range(len(value1)):
                if value1[num] == value2[num]:
                    self.assertEqual(value1[num], value2[num], '程序返回值与计算值不相等')
                else:
                    return 0
    def tearDown(self):
        """

        :return:
        """
        self.log.build_end_line(self.case_name)
        print("测试结束，输出log完结\n\n")
        self.logger.info("测试结束，输出log完结\n\n")
    def executeSQL(self,testid,stem_no,quest_id):
        cand_no_path = os.path.join(proDir, "sql_value.txt")
        with open(cand_no_path, 'r') as f:
            sql_value = f.readline()
        # 查表计算各维度百分位数
        sql_zp_bfs = common.get_sql('ygf_xlcp_20171208', 'standard_normal_info', 'results_value')
        #计算当前量表各维度平均分
        sql_dim_zp_info = common.get_sql('ygf_xlcp_20171208','scr_dimensiongoals','avggoals')
        #各维度的dim_info
        dim_zp_info = configDB.executeSQL_all(sql_dim_zp_info,(sql_value,testid)) #<class 'list'>
        dim_len = len(dim_zp_info)
        #["'自主学习习惯', Decimal('2.00'), 972, 523, 25, Decimal('30.00'), 15", "'学习环境控制', Decimal('2.78'), 972, 523, 25, Decimal('25.00'), 9", "'自主学习倾向', Decimal('3.22'), 972, 523, 25, Decimal('29.00'), 9", "'自主学习情绪', Decimal('2.54'), 972, 523, 25, Decimal('33.00'), 13", "'自主学习效能感', Decimal('2.86'), 972, 523, 25, Decimal('20.00'), 7", "'自主学习意识', Decimal('2.00'), 972, 523, 25, Decimal('16.00'), 8"]
        sql_testid = common.get_sql('ygf_xlcp_20171208', 'user', 'test_id')
        data_value = self.info['data']
        if quest_id == 20:#自评
            print("**************** A-JS ****************")
            print("学生日常行为量表（A-JS） quest_id:%s 学生:%s" % (quest_id, self.student_name))
            print('查询个人各维度平均分sql语句：', sql_dim_zp_info)
            for i in range(dim_len):
                dim_info = eval(dim_zp_info[i])
                # print("****************test_id=%s  quest_id=%s*******************" % (testid, quest_id))
                for j in range(dim_len):
                    if data_value[j]['dim_name'] == dim_info[0] == "自主学习意识":
                        print("^^^^^^^^^^^^^begin %s^^^^^^^^^^^^^" % dim_info[0])
                        self.qj_sql_value(quest_id,dim_info[0],dim_info[1])
                        sql_zp_js_value = self.sql_weidu_value(dim_info[0],sql_zp_bfs,self.zp_zf,dim_info[1],quest_id) #<class 'list'>
                        cx_zp_value = self.cx_weidu_value(data_value,j,dim_info[0],quest_id) #<class 'list'>
                        self.value_asser(sql_zp_js_value, cx_zp_value)
                        print("^^^^^^^^^^^^^end %s^^^^^^^^^^^^^" % dim_info[0])
                    if data_value[j]['dim_name'] == dim_info[0] == "自主学习情绪":
                        print("^^^^^^^^^^^^^begin %s^^^^^^^^^^^^^" % dim_info[0])
                        self.qj_sql_value(quest_id, dim_info[0], dim_info[1])
                        sql_zp_js_value = self.sql_weidu_value(dim_info[0], sql_zp_bfs, self.zp_zf, dim_info[1],quest_id)  # <class 'list'>
                        cx_zp_value = self.cx_weidu_value(data_value, j, dim_info[0], quest_id)  # <class 'list'>
                        self.value_asser(sql_zp_js_value, cx_zp_value)
                        print("^^^^^^^^^^^^^end %s^^^^^^^^^^^^^" % dim_info[0])
                    if data_value[j]['dim_name'] == dim_info[0] == "自主学习倾向":
                        print("^^^^^^^^^^^^^begin %s^^^^^^^^^^^^^" % dim_info[0])
                        self.qj_sql_value(quest_id, dim_info[0], dim_info[1])
                        sql_zp_js_value = self.sql_weidu_value(dim_info[0], sql_zp_bfs, self.zp_zf, dim_info[1],quest_id)  # <class 'list'>
                        cx_zp_value = self.cx_weidu_value(data_value, j, dim_info[0], quest_id)  # <class 'list'>
                        self.value_asser(sql_zp_js_value, cx_zp_value)
                        print("^^^^^^^^^^^^^end %s^^^^^^^^^^^^^" % dim_info[0])
                    if data_value[j]['dim_name'] == dim_info[0] == "自主学习效能感":
                        print("^^^^^^^^^^^^^begin %s^^^^^^^^^^^^^" % dim_info[0])
                        self.qj_sql_value(quest_id, dim_info[0], dim_info[1])
                        sql_zp_js_value = self.sql_weidu_value(dim_info[0], sql_zp_bfs, self.zp_zf, dim_info[1],quest_id)  # <class 'list'>
                        cx_zp_value = self.cx_weidu_value(data_value, j, dim_info[0], quest_id)  # <class 'list'>
                        self.value_asser(sql_zp_js_value, cx_zp_value)
                        print("^^^^^^^^^^^^^end %s^^^^^^^^^^^^^" % dim_info[0])
                    if data_value[j]['dim_name'] == dim_info[0] == "自主学习习惯":
                        print("^^^^^^^^^^^^^begin %s^^^^^^^^^^^^^" % dim_info[0])
                        self.qj_sql_value(quest_id, dim_info[0], dim_info[1])
                        sql_zp_js_value = self.sql_weidu_value(dim_info[0], sql_zp_bfs, self.zp_zf, dim_info[1],quest_id)  # <class 'list'>
                        cx_zp_value = self.cx_weidu_value(data_value, j, dim_info[0], quest_id)  # <class 'list'>
                        self.value_asser(sql_zp_js_value, cx_zp_value)
                        print("^^^^^^^^^^^^^end %s^^^^^^^^^^^^^" % dim_info[0])
                    if data_value[j]['dim_name'] == dim_info[0] == "学习环境控制":
                        print("^^^^^^^^^^^^^begin %s^^^^^^^^^^^^^" % dim_info[0])
                        self.qj_sql_value(quest_id, dim_info[0], dim_info[1])
                        sql_zp_js_value = self.sql_weidu_value(dim_info[0], sql_zp_bfs, self.zp_zf, dim_info[1],quest_id)  # <class 'list'>
                        cx_zp_value = self.cx_weidu_value(data_value, j, dim_info[0], quest_id)  # <class 'list'>
                        self.value_asser(sql_zp_js_value, cx_zp_value)
                        print("^^^^^^^^^^^^^end %s^^^^^^^^^^^^^" % dim_info[0])
        if quest_id ==25:#他评
            print("**************** H-JS ****************")
            print("初中生日常行为家长评定量表（H-JS） quest_id:%s 学生:%s" % (quest_id, self.student_name))
            print('查询个人总维度平均分sql语句：', sql_dim_zp_info)
            for i in range(dim_len):
                dim_info = eval(dim_zp_info[i])
                # print("****************test_id=%s  quest_id=%s*******************" % (testid, quest_id))
                for j in range(dim_len):
                    if data_value[j]['dim_name'] == dim_info[0] == "自主学习意识":
                        print("^^^^^^^^^^^^^begin %s^^^^^^^^^^^^^" % dim_info[0])
                        self.qj_sql_value(quest_id,dim_info[0],dim_info[1])
                        sql_tp_js_value = self.sql_weidu_value(dim_info[0],sql_zp_bfs,self.tp_zf,dim_info[1],quest_id)
                        cx_tp_value = self.cx_weidu_value(data_value,j,dim_info[0],quest_id)
                        self.value_asser(sql_tp_js_value,cx_tp_value)
                        print("^^^^^^^^^^^^^end %s^^^^^^^^^^^^^"%dim_info[0])
                    if data_value[j]['dim_name'] == dim_info[0] == "自主学习情绪":
                        print("^^^^^^^^^^^^^begin %s^^^^^^^^^^^^^" % dim_info[0])
                        self.qj_sql_value(quest_id, dim_info[0], dim_info[1])
                        sql_tp_js_value = self.sql_weidu_value(dim_info[0], sql_zp_bfs, self.tp_zf, dim_info[1],quest_id)
                        cx_tp_value = self.cx_weidu_value(data_value, j, dim_info[0], quest_id)
                        self.value_asser(sql_tp_js_value, cx_tp_value)
                        print("^^^^^^^^^^^^^end %s^^^^^^^^^^^^^" % dim_info[0])
                    if data_value[j]['dim_name'] == dim_info[0] == "自主学习倾向":
                        print("^^^^^^^^^^^^^begin %s^^^^^^^^^^^^^" % dim_info[0])
                        self.qj_sql_value(quest_id, dim_info[0], dim_info[1])
                        sql_tp_js_value = self.sql_weidu_value(dim_info[0], sql_zp_bfs, self.tp_zf, dim_info[1],quest_id)
                        cx_tp_value = self.cx_weidu_value(data_value, j, dim_info[0], quest_id)
                        self.value_asser(sql_tp_js_value, cx_tp_value)
                        print("^^^^^^^^^^^^^end %s^^^^^^^^^^^^^" % dim_info[0])
                    if data_value[j]['dim_name'] == dim_info[0] == "自主学习效能感":
                        print("^^^^^^^^^^^^^begin %s^^^^^^^^^^^^^" % dim_info[0])
                        self.qj_sql_value(quest_id, dim_info[0], dim_info[1])
                        sql_tp_js_value = self.sql_weidu_value(dim_info[0], sql_zp_bfs, self.tp_zf, dim_info[1],quest_id)
                        cx_tp_value = self.cx_weidu_value(data_value, j, dim_info[0], quest_id)
                        self.value_asser(sql_tp_js_value, cx_tp_value)
                        print("^^^^^^^^^^^^^end %s^^^^^^^^^^^^^" % dim_info[0])
                    if data_value[j]['dim_name'] == dim_info[0] == "自主学习习惯":
                        print("^^^^^^^^^^^^^begin %s^^^^^^^^^^^^^" % dim_info[0])
                        self.qj_sql_value(quest_id, dim_info[0], dim_info[1])
                        sql_tp_js_value = self.sql_weidu_value(dim_info[0], sql_zp_bfs, self.tp_zf, dim_info[1],quest_id)
                        cx_tp_value = self.cx_weidu_value(data_value, j, dim_info[0], quest_id)
                        self.value_asser(sql_tp_js_value, cx_tp_value)
                        print("^^^^^^^^^^^^^end %s^^^^^^^^^^^^^" % dim_info[0])
                    if data_value[j]['dim_name'] == dim_info[0] == "学习环境控制":
                        print("^^^^^^^^^^^^^begin %s^^^^^^^^^^^^^" % dim_info[0])
                        self.qj_sql_value(quest_id, dim_info[0], dim_info[1])
                        sql_tp_js_value = self.sql_weidu_value(dim_info[0], sql_zp_bfs, self.tp_zf, dim_info[1],quest_id)
                        cx_tp_value = self.cx_weidu_value(data_value, j, dim_info[0], quest_id)
                        self.value_asser(sql_tp_js_value, cx_tp_value)
                        print("^^^^^^^^^^^^^end %s^^^^^^^^^^^^^" % dim_info[0])
        if quest_id == 22:#他评
            print("**************** C-JS ****************")
            print("初中家长教育行为学生感知量表（C - JS） quest_id:%s 学生:%s" % (quest_id, self.student_name))
            print('查询个人各维度平均分sql语句：', sql_dim_zp_info)
            for i in range(dim_len):
                dim_info = eval(dim_zp_info[i])
                # print("****************test_id=%s  quest_id=%s*******************" % (testid, quest_id))
                for j in range(dim_len):
                    if data_value[j]['dim_name'] == dim_info[0] == "支持态度":
                        print("^^^^^^^^^^^^^begin %s^^^^^^^^^^^^^" % dim_info[0])
                        self.qj_sql_value(quest_id,dim_info[0],dim_info[1])
                        sql_tp_js_value = self.sql_weidu_value(dim_info[0],sql_zp_bfs,self.tp_zf,dim_info[1],quest_id)
                        cx_tp_value = self.cx_weidu_value(data_value,j,dim_info[0],quest_id)
                        self.value_asser(sql_tp_js_value,cx_tp_value)
                        print("^^^^^^^^^^^^^end %s^^^^^^^^^^^^^"%dim_info[0])
                    if data_value[j]['dim_name'] == dim_info[0] == "行为支持":
                        print("^^^^^^^^^^^^^begin %s^^^^^^^^^^^^^" % dim_info[0])
                        self.qj_sql_value(quest_id, dim_info[0], dim_info[1])
                        sql_tp_js_value = self.sql_weidu_value(dim_info[0], sql_zp_bfs, self.tp_zf, dim_info[1],quest_id)
                        cx_tp_value = self.cx_weidu_value(data_value, j, dim_info[0], quest_id)
                        self.value_asser(sql_tp_js_value, cx_tp_value)
                        print("^^^^^^^^^^^^^end %s^^^^^^^^^^^^^" % dim_info[0])
                    if data_value[j]['dim_name'] == dim_info[0] == "情感支持":
                        print("^^^^^^^^^^^^^begin %s^^^^^^^^^^^^^" % dim_info[0])
                        self.qj_sql_value(quest_id, dim_info[0], dim_info[1])
                        sql_tp_js_value = self.sql_weidu_value(dim_info[0], sql_zp_bfs, self.tp_zf, dim_info[1],quest_id)
                        cx_tp_value = self.cx_weidu_value(data_value, j, dim_info[0], quest_id)
                        self.value_asser(sql_tp_js_value, cx_tp_value)
                        print("^^^^^^^^^^^^^end %s^^^^^^^^^^^^^" % dim_info[0])
                    if data_value[j]['dim_name'] == dim_info[0] == "认知支持":
                        print("^^^^^^^^^^^^^begin %s^^^^^^^^^^^^^" % dim_info[0])
                        self.qj_sql_value(quest_id, dim_info[0], dim_info[1])
                        sql_tp_js_value = self.sql_weidu_value(dim_info[0], sql_zp_bfs, self.tp_zf, dim_info[1],quest_id)
                        cx_tp_value = self.cx_weidu_value(data_value, j, dim_info[0], quest_id)
                        self.value_asser(sql_tp_js_value, cx_tp_value)
                        print("^^^^^^^^^^^^^end %s^^^^^^^^^^^^^" % dim_info[0])
        if quest_id == 23:#自评
            print("**************** F-JS ****************")
            print("初中家长教育行为量表（F - JS） quest_id:%s 学生:%s" % (quest_id, self.student_name))
            print('查询个人各维度平均分sql语句：', sql_dim_zp_info)
            for i in range(dim_len):
                dim_info = eval(dim_zp_info[i])
                # print("****************test_id=%s  quest_id=%s*******************" % (testid, quest_id))
                for j in range(dim_len):
                    if data_value[j]['dim_name'] == dim_info[0] == "支持态度":
                        print("^^^^^^^^^^^^^begin %s^^^^^^^^^^^^^" % dim_info[0])
                        self.qj_sql_value(quest_id,dim_info[0],dim_info[1])
                        sql_zp_js_value = self.sql_weidu_value(dim_info[0],sql_zp_bfs,self.zp_zf,dim_info[1],quest_id) #<class 'list'>
                        cx_zp_value = self.cx_weidu_value(data_value,j,dim_info[0],quest_id) #<class 'list'>
                        self.value_asser(sql_zp_js_value, cx_zp_value)
                        print("^^^^^^^^^^^^^end %s^^^^^^^^^^^^^" % dim_info[0])
                    if data_value[j]['dim_name'] == dim_info[0] == "行为支持":
                        print("^^^^^^^^^^^^^begin %s^^^^^^^^^^^^^" % dim_info[0])
                        self.qj_sql_value(quest_id, dim_info[0], dim_info[1])
                        sql_zp_js_value = self.sql_weidu_value(dim_info[0], sql_zp_bfs, self.zp_zf, dim_info[1],quest_id)  # <class 'list'>
                        cx_zp_value = self.cx_weidu_value(data_value, j, dim_info[0], quest_id)  # <class 'list'>
                        self.value_asser(sql_zp_js_value, cx_zp_value)
                        print("^^^^^^^^^^^^^end %s^^^^^^^^^^^^^" % dim_info[0])
                    if data_value[j]['dim_name'] == dim_info[0] == "情感支持":
                        print("^^^^^^^^^^^^^begin %s^^^^^^^^^^^^^" % dim_info[0])
                        self.qj_sql_value(quest_id, dim_info[0], dim_info[1])
                        sql_zp_js_value = self.sql_weidu_value(dim_info[0], sql_zp_bfs, self.zp_zf, dim_info[1],quest_id)  # <class 'list'>
                        cx_zp_value = self.cx_weidu_value(data_value, j, dim_info[0], quest_id)  # <class 'list'>
                        self.value_asser(sql_zp_js_value, cx_zp_value)
                        print("^^^^^^^^^^^^^end %s^^^^^^^^^^^^^" % dim_info[0])
                    if data_value[j]['dim_name'] == dim_info[0] == "认知支持":
                        print("^^^^^^^^^^^^^begin %s^^^^^^^^^^^^^" % dim_info[0])
                        self.qj_sql_value(quest_id, dim_info[0], dim_info[1])
                        sql_zp_js_value = self.sql_weidu_value(dim_info[0], sql_zp_bfs, self.zp_zf, dim_info[1],quest_id)  # <class 'list'>
                        cx_zp_value = self.cx_weidu_value(data_value, j, dim_info[0], quest_id)  # <class 'list'>
                        self.value_asser(sql_zp_js_value, cx_zp_value)
                        print("^^^^^^^^^^^^^end %s^^^^^^^^^^^^^" % dim_info[0])
    def checkResult(self):
        """
        check test result
        :return:
        """
        self.info = self.return_json.json()
        data_value = self.info['data']
        common.show_return_msg(self.return_json)
        if self.info['code'] == 0:
            self.log.build_sql_line(self.case_name)
            with open('E:/XYRGInterface/testCase/user/sql_value.txt', 'r') as f:
                sql_value = f.readline()
            print("开始连接数据库......")
            self.logger.info("开始连接数据库......")
            sql_testid = common.get_sql('ygf_xlcp_20171208', 'user', 'test_id')
            # 根据学校和学号
            cursor_sql_value_testid = configDB.executeSQL_all(sql_testid, (self.student_name,sql_value))
            number = len(cursor_sql_value_testid)
            if self.type == '学生':
                for i in range(number):
                    testid = cursor_sql_value_testid[i]
                    # print(testid)
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
        common.get_value_from_return_json_assertEqual(self.info, 'code', 'msg', self.case_name)
        # if self.result == '0':
        #     # common.get_value_from_return_json_assertEqual(self.info, 'code', 'msg',self.case_name)
        #     self.assertEqual(self.info['code'], self.code,"code值验证不成功")
        #     self.assertEqual(self.info['msg'], self.msg,"msg值验证不成功")
        # if self.result == '1':
        #     self.assertEqual(self.info['code'], self.code,"code值验证不成功")
        #     self.assertEqual(self.info['msg'], self.msg,"msg值验证不成功")
