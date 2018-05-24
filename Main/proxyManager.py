'''
    控制代理ip池运行的主程序
'''
import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
from Scheduler.getSourceProxies import get_source_proxies
import time
from DB.redisClient import RedisConn
from Scheduler.checkSourceProxies import CheckProxy
from Scheduler.refreshUsefulProxy import RefreshProxy
import redis

refresh_interval = 600 # 更新已有代理的时间间隔
min_useful_proxies_num = 50 # 有效代理少与该值时，重新获取免费ip

redis_conn = redis.StrictRedis(host='localhost', port=6379, db=3)

if __name__ == '__main__':
    rp = RefreshProxy(redis_conn)
    cp = CheckProxy(redis_conn)
    try:# 验证redis是否连接
        redis_conn.ping()
    except:
        redis_conn = redis.StrictRedis(host='localhost', port=6379, db=3)

    refresh_time = time.time()
    first_refresh = True
    while True:
        if time.time() - refresh_time > refresh_interval or first_refresh:
            refresh_time = time.time()
            print('重新检验UsefulProxy中ip的有效性...')
            print(rp.refresh_main())
            first_refresh = False


        if len(RedisConn.get_all_hash('UsefulProxy',redis_conn=redis_conn)) <= min_useful_proxies_num:
            print('可用ip数不足100，重新抓取免费ip...')
            free_proxies = get_source_proxies()
            print('共获取免费ip{}个'.format(sum([len(i) for i in free_proxies])))
            print('开始检查获取免费ip')
            # free_proxies = [['192.168.2.100:8081','127.0.0.1:1080'], ['127.0.0.1:1080','127.0.0.1:1080']]
            for proxies_list in free_proxies:
                if proxies_list:
                    cp.check_main(proxies_list)
            print('检查完成')

        print('代理池开启中...')
        time.sleep(100)
