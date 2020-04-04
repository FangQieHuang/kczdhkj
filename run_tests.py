import time, sys
sys.path.append('./interface')
sys.path.append('./sb_fixture')
from HTMLTestRunner import HTMLTestRunner
#import HTMLTestRunner
import unittest
from db_fixture import test_data



#制定测试用例为当前文件夹下的interface目录
test_dir = './interface'
discover = unittest.defaultTestLoader.discover(test_dir, pattern='*_test.py')



if __name__ == "__main__":
    test_data.init_data() #初始化接口测试数据

    now = time.strftime("%Y-%m-%d %H-%M-%S")
    filename = './report/' + now + '_result.html'
    fp = open(filename, 'wb')
    runner = HTMLTestRunner(stream=fp,
                            title='库存服务管理系统接口自动化测试',
                            description='运行环境：MySQL(PyMySQL), Requests, unittest ')
    print(discover)
    runner.run(discover)
    fp.close()