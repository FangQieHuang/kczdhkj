import sys, time
sys.path.append('../db_fixture')
try:
    from mysql_db import DB
except ImportError:
    from .mysql_db import DB

# 定义过去时间
past_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()-100000))

# 定义将来时间
future_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()+10000))



# create data创建测试数据
datas = {
    't_stock':[
        {'FstrAgentAppId':'京东a','FstrProductId':'京东a0001','`FuiRealityStock`':10,'FuiAvailableStockNum':10},
        {'FstrAgentAppId': '淘宝a', 'FstrProductId': '淘宝a0001', '`FuiRealityStock`': 20, 'FuiAvailableStockNum': 20},
        {'FstrAgentAppId': '网易a', 'FstrProductId': '网易a0001', '`FuiRealityStock`': 30, 'FuiAvailableStockNum': 30},
    ],
    't_product_in_stock_flow':[
        {'FstrOperator':'FQH','FuiInStockNum':10,'FuiInStockType':0,'FstrSerialNo':'1','FuiStockId':'1'},
        {'FstrOperator': 'FQH', 'FuiInStockNum': 20, 'FuiInStockType': 0,'FstrSerialNo':'2','FuiStockId':'2'},
        {'FstrOperator':'FQH','FuiInStockNum':30,'FuiInStockType':0,'FstrSerialNo':'3','FuiStockId':'3'},
    ],
}


# Inster table datas
def init_data():
    db = DB()
    for table, data in datas.items():
        db.clear(table)
        for d in data:
            db.insert(table, d)
    db.close()


if __name__ == '__main__':
    init_data()
