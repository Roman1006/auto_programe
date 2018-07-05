#coding:utf-8
import readConfig
import os
from datetime import datetime
import logging
import threading
import codecs


localReadConfig = readConfig.ReadConfig()

class Log:
    def __init__(self):
        #定义全局变量
        global logPath, resultPath, proDir
        proDir = readConfig.proDir
        #result目录路径
        resultPath = os.path.join(proDir,"result")
        #判断result目录是否存在，如果不存在则创建
        if not os.path.exists(resultPath):
            os.mkdir(resultPath)
        #定义log文件名称，以格式化时间命名
        logPath = os.path.join(resultPath,str(datetime.now().strftime("%Y%m%d%H%M%S")))
        print(logPath)

        if not os.path.exists(logPath):
            os.mkdir(logPath)
        # 生成self.logger对象
        self.logger = logging.getLogger()
        # 设定logger等级
        self.logger.setLevel(logging.INFO)

        # 定义handler 写入文件
        handler = logging.FileHandler(os.path.join(logPath,"output.log"))
        # 定义formatter 显示在控制台
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        # self.logger.addFilter(formatter)


    def get_logger(self):
        return self.logger

    def build_start_line(self,case_name):
        self.logger.info(u"--------" + case_name + " START--------")

    def build_sql_line(self,case_name):
        self.logger.info("--------" + case_name +"SQL_START--------")

    def build_end_line(self,case_name):
        self.logger.info(u"--------" + case_name + " END--------")

    def build_case_line(self,case_name,code,msg):
        self.logger.info("_____________________________")

    def get_report_path(self):
        report_path = os.path.join(logPath,"report.html")
        return report_path

    def get_result_path(self):
        return logPath

    def write_result(self,result):
        result_path = os.path.join(logPath,"report.txt")
        fb = open(result_path,"wb")
        try:
            fb.write(result)
        except FileNotFoundError as ex:
            logging.error(str(ex))


class MyLog:
    log = None
    mutex = threading.Lock()

    def __init__(self):
        pass

    @staticmethod
    def get_log():
        if MyLog.log is None:
            MyLog.mutex.acquire()
            MyLog.log = Log()
            MyLog.mutex.release()

        return MyLog.log

if __name__ == "__main__":
    log = MyLog.get_log()
    logger = log.get_logger()
    logger.debug("test debug")
    logger.info("test info")
    file = codecs.open("output.log", 'r', 'utf-8')
    for i in file:
        print(type(i))

