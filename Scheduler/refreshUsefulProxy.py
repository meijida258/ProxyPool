from DB.redisClient import RedisConn
from Util.checkProxy import check_proxy
import asyncio

'''
    定时触发的检验有效ip列表中的ip，更新有效ip信息，删除失效ip
'''

class RefreshProxy:
    def refresh_result(self, refresh_proxies):
        useful_count = 0
        for result in refresh_proxies:
            if result.pop('type') == 1:
                score = 100 - (result['used_time'] - 1) * 5 if (100 - (result['used_time'] - 1) * 5) > 0 else 0
                rc.push_hash('UsefulProxy', {result['proxy']: int(score)})
                useful_count += 1
            else:
                rc.del_hash('UsefulProxy', result['proxy'])
        return '验证{}个ip，有效ip:{}个,失效ip：{}个'.format(len(refresh_proxies), useful_count, len(refresh_proxies)-useful_count)
    
    def refresh_main(self):
        rc = RedisConn()
        useful_proxies = rc.get_all_hash('UsefulProxy')
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