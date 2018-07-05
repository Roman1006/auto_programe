#coding:utf-8
import readConfig
from common.Log import MyLog as Log
import requests
import urllib
import http.cookiejar
import codecs
import urllib.request
import os


localReadConfig = readConfig.ReadConfig()
proDir = os.path.split(os.path.realpath(__file__))[0]
prodir = os.path.dirname(proDir)

class ConfigHttp:

    def __init__(self):
        global scheme, host, port, timeout
        scheme = localReadConfig.get_http("scheme")
        host = localReadConfig.get_http("baseurl")
        port = localReadConfig.get_http("port")
        timeout = localReadConfig.get_http("timeout")
        self.log = Log.get_log()
        self.logger = self.log.get_logger()
        self.headers = {
        "User-Agent": "Apache-HttpClient/4.5.3 (Java/1.8.0_131)",
        "host":"test2.yuangaofen.com",
        "Connection": "keep-alive",
        "Content-Type": "application/json;charset=UTF-8",
        }
        self.params = {}
        self.data = {}
        self.url = None  #http://test3.yuangaofen.com/xlcp/UserBind/testLoginTwo
        self.files = {}
        self.state = 0
        self.cookies = {}
        self.number = {}


    def set_url(self,url):
        self.url = url

    # def set_cookie(self,cookie):
    #     self.cookies = cookie

    def set_cookies(self,cookie):
        self.cookies = cookie
        return self.cookies

    def set_header(self,header):
        self.headers = header
        return self.headers

    def set_params(self,param):
        self.params = param
        return self.params

    def set_stu_test_code(self,number):
        self.number = number
        return self.number

    # def get_stu_test_code(self):

    def set_data(self,data):
        self.data = data
        return self.data

    def set_files(self,filename):
        if filename!='':
            file_path = prodir+'/testFile/img/'+ filename
            self.files = {'file': open(file_path, 'rb')}
        if filename == '' or filename is None:
            self.state = 1

    def get(self):
        try:
            # test_session = requests.session()
            # response = test_session.get(self.url, headers=self.headers, params=self.params, timeout=float(timeout))
            # print(response.text)
            # print(response.status_code)
            # print(response.cookies)

            response = requests.get(self.url, headers=self.headers, params=self.params, timeout=float(timeout))
            # print("djskfhkjsdhf")
            # print(response.cookies)

            # req = urllib.request.Request(self.url,self.params,self.headers)
            # resp = req.urlopen(req)
            # page = resp.read()
            # the_page = page.decode("utf-8")
            # b_page = the_page.encode("utf-8")
            # # req.decode()
            # cj = http.cookiejar.CookieJar()
            # print(45679456)
            # print(cj)
            # opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
            # # r = opener.open(req)
            # # print(r.read())
            #print(response.headers['Set-Cookie'])
            # print(response)

            return response
        except TimeoutError:
            self.logger.error("Time out!")
            return None

    def post(self):
        try:
            # print(self.url)
            # print(self.data)
            # print(456789)
            # print(self.headers)
            response = requests.post(self.url, headers=self.headers, data=self.data)
            return response

        except TimeoutError:
            self.logger.error("Time out!")
            return None

    def postWriteFile(self):
        try:
            response = requests.post(self.url, headers=self.headers, data=self.data, files=self.files, timeout=float(timeout))
            return response
        except TimeoutError:
            self.logger.error("Time out!")
            return None

    def postWriteJson(self):
        try:
            response = requests.post(self.url, headers=self.headers, json=self.data, timeout=float(timeout),cookies=self.cookies)
            return response
        except TimeoutError:
            self.logger.error("Time out!")
            return None


if __name__ == "__main__":
    print("ConfigHTTP")