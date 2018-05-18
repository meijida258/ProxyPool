'''
    获取免费ip，返回ip列表结果，采用多进程
'''
import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
from GetProxies.getFreeProxies import GetProxies
from multiprocessing import Pool as ProcessPool
from Util.getConfig import GetConfig

def run_cls_func(func_name):
    return getattr(GetProxies, func_name)()

def get_source_proxies():
    get_config = GetConfig()
    # 获取免费代理的所有方法名字
    proxy_func_names = get_config.get_proxy_func()
    # 多进程获取免费代理
    pool = ProcessPool(4)
    result = pool.map(run_cls_func, proxy_func_names)
    pool.close()
    pool.join()
    # 将[[proxy, proxy, ...], [proxy, proxy, ...]]返回
    return result

if __name__ == '__main__':
    result = get_source_proxies()

