import pymysql
import readConfig
from common.Log import MyLog as Log

localReadConfig = readConfig.ReadConfig()


class MyDB:
    def __init__(self):
        global host, username, password, port, database, config
        host = localReadConfig.get_db("host")
        username = localReadConfig.get_db("username")
        password = localReadConfig.get_db("password")
        port = localReadConfig.get_db("port")
        database = localReadConfig.get_db("database")
        use_unicode = True
        charset = localReadConfig.get_db("charset")
        config = {
            'host': str(host),
            'user': username,
            "password": password,
            "port": int(port),
            'db': database,
            'use_unicode': use_unicode,
            'charset': str(charset)
        }
        # 'charset': str(charset)
        self.log = Log.get_log()
        self.logger = self.log.get_logger()
        self.db = None
        self.cursor = None

    def connectDB(self):
        try:
            # 链接db
            self.db = pymysql.connect(**config)
            # 创建游标
            self.cursor = self.db.cursor()
            # print("Connect DB sucessfully!")
            self.logger.error("Connect DB sucessfully!")
        except ConnectionError as ex:
            self.logger.error(str(ex))

    # ,params
    def executeSQL(self,sql,params):
        # print(params)
        self.connectDB()
        self.cursor.execute(sql,params)
        self.db.commit()
        value = self.cursor.fetchone()[0]
        # print(value)
        # print(type(value))
        return value

    def executeSQL_all(self,sql,params):
        # print(params)
        test_id = []
        test_id_input = []
        self.connectDB()
        num = self.cursor.execute(sql,params)
        self.db.commit()
        for each in self.cursor.fetchmany(num):
            # print(each)
            test_id.append("".join(str(list(each))))
        for i in range(num):
            test_id_in = str(test_id[i])[int(str(test_id[i]).find('[')) + 1:int(str(test_id[i]).find(']'))]
            test_id_input.append("".join(test_id_in))
        # print(test_id_input)
        return test_id_input


    def get_all(self, cursor):
        value = cursor.fetchall()
        return value

    def get_one(self,cursor):
        value = cursor.fetchone()
        return value

    def closeDB(self):
        self.db.close()
        print("Database closed!")