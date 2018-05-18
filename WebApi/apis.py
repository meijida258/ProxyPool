'''
    根据请求参数，返回代理
'''
from DB.redisClient import RedisConn
import random

def get_proxy(count, score=-1):
    rc = RedisConn()
    useful_proxies = rc.get_all_hash('UsefulProxy', result_type=2)
    if int(score) > 0:
        useful_proxies = sorted(useful_proxies, key=lambda i:int(list(i.values())[0]), reverse=True)
        if len(useful_proxies) < count:
            return [list(item.keys())[0] for item in useful_proxies]
        return [list(item.keys())[0] for item in useful_proxies[:count]]
    else:
        random.shuffle(useful_proxies)
        if len(useful_proxies) < count:
            return [list(item.keys())[0] for item in useful_proxies]
        return [list(item.keys())[0] for item in useful_proxies[:count]]

