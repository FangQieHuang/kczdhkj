# coding=utf8
import pymysql.cursors
from os.path import abspath, dirname
import configparser as cparser
import time as time
import uuid


# ======== Reading db_config.ini setting ===========
base_dir = dirname(dirname(abspath(__file__)))
base_dir = base_dir.replace('\\', '/')
file_path = base_dir + "/db_config.ini"

cf = cparser.ConfigParser()

cf.read(file_path)
host = cf.get("mysqlconf", "host")
port = cf.get("mysqlconf", "port")
db   = cf.get("mysqlconf", "db_name")
user = cf.get("mysqlconf", "user")
password = cf.get("mysqlconf", "password")


# ======== MySql base operating ===================
class DB:

    def __init__(self):
        try:
            # Connect to the database
            self.connection = pymysql.connect(host=host,
                                              port=int(port),
                                              user=user,
                                              password=password,
                                              db=db,
                                              charset='utf8mb4',
                                              cursorclass=pymysql.cursors.DictCursor)
        except pymysql.err.OperationalError as e:
            print("Mysql Error %d: %s" % (e.args[0], e.args[1]))

    # clear table data
    def clear(self, table_name):
        # real_sql = "truncate table " + table_name + ";"
        real_sql = "delete from " + table_name + ";"
        # print("清除表数据 : sql = " + real_sql)
        with self.connection.cursor() as cursor:
            # cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
            cursor.execute(real_sql)
        self.connection.commit()

    # insert sql statement
    def insert(self, table_name, table_data):
        for key in table_data:
            table_data[key] = "'"+str(table_data[key])+"'"
        key   = ','.join(table_data.keys())
        value = ','.join(table_data.values())
        real_sql = "INSERT INTO " + table_name + " (" + key + ") VALUES (" + value + ")"
        # print("新增数据 : sql = " + real_sql)

        with self.connection.cursor() as cursor:
            cursor.execute(real_sql)

        self.connection.commit()

    # close database
    def close(self):
        self.connection.close()

    # init data
    def init_data(self, datas):
        for table, data in datas.items():
            self.clear(table)
            for d in data:
                self.insert(table, d)
        self.close()

    def find_stock_id_by_FstrAgentAppId_and_FstrProductId(self, FstrAgentAppId, FstrProductId):
        # real_sql = "truncate table " + table_name + ";"
        real_sql = "select FuiId from t_stock where FstrAgentAppId = '"+ FstrAgentAppId +"' and FstrProductId = '"+ FstrProductId +"'"
        # print("清除表数据 : sql = " + real_sql)
        with self.connection.cursor() as cursor:
            cursor.execute(real_sql)
            stock_id2 = cursor.fetchone()  #fetchone()获取第一条结果，返回单个元组如('id','title',这里是{'FuiId': 1584861529})
            # print(stock_id2)
        self.connection.commit()
        return stock_id2


if __name__ == '__main__':
    db = DB()
    stock_table_name = "t_stock"
    t_product_in_stock_flow_table_name = "t_product_in_stock_flow"
    # db.clear(stock_table_name)
    # db.clear(t_product_in_stock_flow_table_name)


    stock_data = {'FstrAgentAppId':'京东a','FstrProductId':'京东a0001','`FuiRealityStock`':10,'FuiAvailableStockNum':10}
    db.insert(stock_table_name, stock_data)
    current_serial_no = uuid.uuid1()

    stock_id_dict = db.find_stock_id_by_FstrAgentAppId_and_FstrProductId("京东a", '京东a0001')  #{'FuiId': 1584861529})
    stock_id = stock_id_dict['FuiId']  #获取FuiId的value：1584861529
    t_product_in_stock_flow_data = {'FstrOperator':'FQH','FuiInStockNum':10,'FuiInStockType':0,'FuiStockId':stock_id,'FstrSerialNo':current_serial_no}
    db.insert(t_product_in_stock_flow_table_name, t_product_in_stock_flow_data)

    db.close()
