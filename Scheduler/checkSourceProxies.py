'''
    检验获得的免费ip有效性，并将结果保存
'''
import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
from DB.redisClient import RedisConn
from Util.checkProxy import main
import asyncio

class CheckProxy:
    def __init__(self, redis_conn):
        self.redis_conn = redis_conn

    def check_results(self, check_proxies):
        useful_count = 0
        for result in check_proxies:
            if result.pop('type') == 1:
                score = 5
                RedisConn.push_hash('UsefulProxy', {result['proxy']:int(score)}, redis_conn=self.redis_conn)
                useful_count += 1
            # rc.del_list_item('SourceProxy', check_result['proxy'])
        return '验证{}个ip，有效ip:{}个,失效ip：{}个'.format(len(check_proxies), useful_count, len(check_proxies)-useful_count)

    def check_main(self, proxies_list):
        '''
        :param proxies_list:需要验证的ip
        :return:
        '''
        # 验证sourceProxy
        # loop = asyncio.get_event_loop()
        # check_result = []
        # tasks = [check_proxy(proxies, check_result) for proxies in proxies_list]
        # loop.run_until_complete(asyncio.wait(tasks))
        check_result = main(proxies_list)
        # 根据结果保存usefulProxy
        print(self.check_results(check_result))

if __name__ == '__main__':
    rc = RedisConn()
else:
    rc = RedisConn()