from Scheduler.getSourceProxies import get_source_proxies
import time
from DB.redisClient import RedisConn
from Scheduler.checkSourceProxies import CheckProxy
from Scheduler.refreshUsefulProxy import RefreshProxy

'''
    控制代理ip池运行的主程序
'''

refresh_interval = 7200 # 更新已有代理的时间间隔
min_useful_proxies_num = 50 # 有效代理少与该值时，重新获取免费ip

rc = RedisConn()
rp = RefreshProxy()
cp = CheckProxy()

if __name__ == '__main__':

    refresh_time = time.time()
    while True:
        if len(rc.get_all_hash('UsefulProxy')) <= min_useful_proxies_num:
            print('可用ip数不足100，重新抓取免费ip...')
            free_proxies = get_source_proxies()
            print('共获取免费ip{}个'.format(sum([len(i) for i in free_proxies])))
            print('开始检查获取免费ip')
            # free_proxies = [['192.168.2.100:8081','127.0.0.1:1080'], ['127.0.0.1:1080','127.0.0.1:1080']]
            for proxies_list in free_proxies:
                if proxies_list:
                    cp.check_main(proxies_list)
            print('检查完成')

        if time.time() - refresh_time > refresh_interval:
            refresh_time = time.time()
            print('重新检验UsefulProxy中ip的有效性...')
            print(rp.refresh_main())

        time.sleep(300)