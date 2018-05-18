'''
    检验获得的免费ip有效性，并将结果保存
'''
from DB.redisClient import RedisConn
from Util.checkProxy import check_proxy
import asyncio

class CheckProxy:
    def check_results(self, check_proxies):
        useful_count = 0
        for result in check_proxies:
            if result.pop('type') == 1:
                score = 100 - (result['used_time']-1)*5 if (100 - (result['used_time']-1)*5) > 0 else 0
                rc.push_hash('UsefulProxy', {result['proxy']:int(score)})
                useful_count += 1
            # rc.del_list_item('SourceProxy', check_result['proxy'])
        return '验证{}个ip，有效ip:{}个,失效ip：{}个'.format(len(check_proxies), useful_count, len(check_proxies)-useful_count)

    def check_main(self, proxies_list):
        '''
        :param proxies_list:需要验证的ip
        :return:
        '''
        # 验证sourceProxy
        loop = asyncio.get_event_loop()
        check_result = []
        tasks = [check_proxy(proxies, check_result) for proxies in proxies_list]
        loop.run_until_complete(asyncio.wait(tasks))
        # 根据结果保存usefulProxy
        print(self.check_results(check_result))

if __name__ == '__main__':
    rc = RedisConn()
else:
    rc = RedisConn()