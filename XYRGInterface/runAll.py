#coding:utf-8
import os
import unittest
from common.Log import MyLog as Log
import readConfig as readConfig
from common import HTMLTestRunner
from common.configEmail import MyEmail
import urllib
import http.cookiejar

localReadConfig = readConfig.ReadConfig()


class AllTest:
    def __init__(self):
        global log, logger, resultPath, on_off, cookie
        log = Log.get_log()
        logger = log.get_logger()
        resultPath = log.get_report_path()
        on_off = localReadConfig.get_email("on_off")
        # cookie = localReadConfig.
        self.caseListFile = os.path.join(readConfig.proDir, "caselist.txt")
        self.caseFile = os.path.join(readConfig.proDir, "testCase")
        self.cookie = os.path.join(readConfig.proDir, "testFile", "case", 'cookie.txt')
        # self.caseFile = None
        self.caseList = []
        self.email = MyEmail.get_email()

    def set_case_list(self):
        """
        set case list
        :return:
        """
        fb = open(self.caseListFile)
        for value in fb.readlines():
            data = str(value)
            # print(data)
            if data != '' and not data.startswith("#"):
                self.caseList.append(data.replace("\n", ""))
        return self.caseList
        fb.close()

    def set_case_suite(self):
        """
        set case suite
        :return:
        """
        self.set_case_list()
        # 初始化一个测试套件
        test_suite = unittest.TestSuite()
        suite_module = []

        for case in self.caseList:
            case_name = case.split("/")[-1]
            print("******************test_case begin******************")
            print(case_name+".py")
            # discover返回的是一个list集合 pattern=case_name + '.py'
            discover = unittest.defaultTestLoader.discover(self.caseFile, pattern=case_name + '.py',top_level_dir=None)
            suite_module.append(discover)
            # print("******************test_case end******************")


        if len(suite_module) > 0:

            for suite in suite_module:
                for test_name in suite:
                    test_suite.addTest(test_name)
        else:
            return None

        return test_suite

    def run(self):
        """
        run test
        :return:
        """
        try:
            suit = self.set_case_suite()
            # print(suit)
            if suit is not None:
                logger.info("********TEST START********")
                print("******************TEST START******************")
                fp = open(resultPath, 'wb')
                runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title='Test Report', description='Test Description')
                runner.run(suit)
            else:
                logger.info("Have no case to test.")
        except Exception as ex:
            print("跑不到用例里面去呀")
            logger.error(str(ex))
        finally:
            logger.info("*********TEST END*********")
            print("******************TEST END******************")
            # fp.close()
            # send test report by email
            if on_off == 'on':
                self.email.send_email()
                logger.info("The test report has send to developer by email.")
            elif on_off == 'off':
                logger.info("Doesn't send report email to developer.")
            else:
                logger.info("Unknow state.")


if __name__ == '__main__':
    obj = AllTest()
    obj.run()
