# coding:utf-8
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from datetime import datetime
import threading
import readConfig
from common.Log import MyLog
import zipfile
import glob

localReadConfig = readConfig.ReadConfig()

class Email:
    def __init__(self):
        global host, user, password, port, sender, content, title
        host = localReadConfig.get_email("mail_host")
        user = localReadConfig.get_email("mail_user")
        password = localReadConfig.get_email("mail_pass")
        port = localReadConfig.get_email("mail_port")
        sender = localReadConfig.get_email("sender")
        title = localReadConfig.get_email("subject")
        content = localReadConfig.get_email("content")

        self.value = localReadConfig.get_email("receiver")
        self.receiver = []
        for n in str(self.value).split("/"):
            self.receiver.append(n)

        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.subject = "学业人格接口测试报告" + " " + date

        self.log = MyLog.get_log()
        self.logger = self.log.get_logger()
        self.msg = MIMEMultipart('related')

    def config_header(self):
        self.msg['subject'] = self.subject
        self.msg['from'] = sender
        self.msg['to'] = ";".join(self.receiver)

    def config_content(self):
        f = open(os.path.join(readConfig.proDir,'testFile','emailStyle.txt'))
        content = f.read()
        f.close()
        content_plain = MIMEText(content,'html','UTF-8')
        self.msg.attach(content_plain)
        self.config_image()

    def config_image(self):
        imagel_path = os.path.join(readConfig.proDir,'testFile','img','1.png')
        fp1 = open(imagel_path,'rb')
        msgImage1 = MIMEImage(fp1.read())
        fp1.close()

        msgImage1.add_header("Content-ID",'<image1>')
        self.msg.attach(msgImage1)

        image2_path = os.path.join(readConfig.proDir,'testFile', 'img', 'logo.png')
        fp2 = open(image2_path,'rb')
        msgImage2 =MIMEImage(fp2.read())
        fp2.close()

        msgImage2.add_header('Content-ID', '<image2>')
        self.msg.attach(msgImage2)

    def config_file(self):

        if self.check_file():
            reportpath = self.log.get_result_path()
            jss = os.path.abspath(os.path.dirname("echarts.common.min.js"))
            zippath = os.path.join(readConfig.proDir, "result", "interface_test.zip")

            files = glob.glob(reportpath+'\*')
            f = zipfile.ZipFile(zippath,'w',zipfile.ZIP_DEFLATED)
            for file in files:
                f.write(file, '/report/'+os.path.basename(file))
            f.close()

            reportfile = open(zippath,'rb').read()
            filehtml = MIMEText(reportfile,'base64','utf-8')
            filehtml['Content-Type'] = 'application/octet-stream'
            filehtml['Content-Disposition'] = 'attachment; filename="interface_test.zip"'
            self.msg.attach(filehtml)

    def check_file(self):
        reportpath = self.log.get_report_path()
        if os.path.isfile(reportpath) and not os.stat(reportpath) == 0:
            return True
        else:
            return False

    def send_email(self):
        self.config_header()
        self.config_content()
        self.config_file()
        try:
            smtp = smtplib.SMTP()
            smtp.connect(host)
            smtp.login(user,password)
            smtp.sendmail(sender,self.receiver,self.msg.as_string())
            smtp.quit()
            self.logger.info("The test report has send to developer by email.")
        except Exception as ex:
            self.logger.error(str(ex))

class MyEmail:
    email = None
    mutex = threading.Lock()

    def __init__(self):
        pass

    @staticmethod
    def get_email():

        if MyEmail.email is None:
            MyEmail.mutex.acquire()
            MyEmail.email = Email()
            MyEmail.mutex.release()
        return MyEmail.email

if __name__ == "__main__":
    email = MyEmail.get_email()