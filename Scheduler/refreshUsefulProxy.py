'''
    定时触发的检验有效ip列表中的ip，更新有效ip信息，删除失效ip
'''
import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
from DB.redisClient import RedisConn
from Util.checkProxy import check_proxy
import asyncio

class RefreshProxy:
    def __init__(self, redis_conn):
        self.redis_conn = redis_conn
    def refresh_result(self, refresh_proxies):
        useful_count = 0
        for result in refresh_proxies:
            if result.pop('type') == 1:
                score = 5
                rc.push_hash('UsefulProxy', {result['proxy']: int(score)}, redis_conn=self.redis_conn)
                useful_count += 1
            else:
                score = int(rc.get_by_key(hash_name='UsefulProxy', redis_conn=self.redis_conn, key=result['proxy']))
                if score == 1:
                    rc.del_hash('UsefulProxy', result['proxy'], redis_conn=self.redis_conn)
                else:
                    rc.push_hash('UsefulProxy', {result['proxy']: int(score)-1}, redis_conn=self.redis_conn)
        return '验证{}个ip，有效ip:{}个,失效ip：{}个'.format(len(refresh_proxies), useful_count, len(refresh_proxies)-useful_count)

    def refresh_main(self):
        rc = RedisConn()
        useful_proxies = rc.get_all_hash('UsefulProxy', redis_conn=self.redis_conn)
        # 验证useful_proxies
        loop = asyncio.get_event_loop()
        refresh_proxies = []
        tasks = [check_proxy(proxies, refresh_proxies) for proxies in useful_proxies]
        loop.run_until_complete(asyncio.wait(tasks))

        refresh_log = self.refresh_result(refresh_proxies)
        return refresh_log

if __name__ == '__main__':
    rc = RedisConn()
else:
    rc = RedisConn()