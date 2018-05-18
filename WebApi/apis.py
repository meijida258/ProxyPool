'''
    根据请求参数，返回代理
'''
import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from DB.redisClient import RedisConn
import random

def get_proxy(count, score=-1):
    rc = RedisConn()
    useful_proxies = rc.get_all_hash('UsefulProxy', result_type=2)
    if int(score) > 0:
        insert_proxy = {'localhost':score}
        useful_proxies.append(insert_proxy)
        useful_proxies = sorted(useful_proxies, key=lambda i:int(list(i.values())[0]), reverse=True)
        if len(useful_proxies) <= count: # 请求的数量超过已有ip的总数，返回所有ip
            return [list(item.keys())[0] for item in useful_proxies]
        # 请求的数量小于已有ip的总数，取出大于请求分数的ip，再随机排序，最后返回请求数的ip
        shuffle_proxies_list = [list(item.keys())[0] for item in useful_proxies[:useful_proxies.index(insert_proxy)]]
        random.shuffle(shuffle_proxies_list)
        return shuffle_proxies_list[:count]
    else:
        random.shuffle(useful_proxies)
        if len(useful_proxies) < count:
            return [list(item.keys())[0] for item in useful_proxies]
        return [list(item.keys())[0] for item in useful_proxies[:count]]

