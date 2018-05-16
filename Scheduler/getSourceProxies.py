from GetProxies.getFreeProxies import GetProxies
from multiprocessing import Pool as ProcessPool
from Util.getConfig import GetConfig

#
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

