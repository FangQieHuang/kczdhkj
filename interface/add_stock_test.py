import unittest
import requests
import os, sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)
from db_fixture import test_data

class SearchStockTest(unittest.TestCase):

    def setUp(self):
        self.base_url = "http://127.0.0.1:1751/search/stock"

    def tearDown(self):
        print(self.result)

    def test_search_stock_by_FstrProductId(self):
        '''通过FstrProductId查找库存'''
        payload = {"agentAppId": "京东a" , "productId": "京东a0001"}
        r = requests.post(self.base_url, None, payload)
        # print("post 请求 url = %s, params = %s, reponse = %s" %(self.base_url, payload, r.json()))
        # print(r)
        # print('123')
        self.result = r.json()
        # print(self.result)
        self.assertEqual(self.result['code'], 0)
        self.assertEqual(self.result['msg'], 'ok')


if __name__ == '__main__':
    test_data.init_data()
    unittest.main()
