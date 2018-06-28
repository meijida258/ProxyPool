'''
    异步访问验证网站，快速检验ip有效性,返回检验结果
'''
import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
from Util.getConfig import GetConfig
import aiohttp, asyncio
import time

check_url = GetConfig().config['CHECKINFO']['check_url']
check_keywords = GetConfig().config['CHECKINFO']['check_keywords'].split('|')

async def check_proxy(proxy, check_result):
    async with aiohttp.ClientSession() as session:
        try:
            start_time = time.clock()
            async with session.get(url=check_url, proxy='http://{}'.format(proxy), timeout=30) as response:
                response_ = await response.text()
                if any(check_keyword in response_ for check_keyword in check_keywords):
                    check_result.append({'used_time':time.clock()-start_time, 'proxy':proxy, 'type':1})
                    return check_result
                else:
                    check_result.append({'type':0, 'proxy':proxy})
                    return check_result
        except Exception as e:
            print('使用ip:{}访问出错：{}'.format(proxy, e))
            check_result.append({'type': 0, 'proxy': proxy})
            return check_result

# 使用一个session测试代理
async def check_one(proxy, session):
    try:
        start_time = time.clock()
        async with session.get(url=check_url, proxy='http://{}'.format(proxy), timeout=30) as res:
            res_ = await res.text()
            if any(check_keyword in res_ for check_keyword in check_keywords):
                return {'used_time': time.clock() - start_time, 'proxy': proxy, 'type': 1}
            else:
                return {'type': 0, 'proxy': proxy}
    except Exception as e:
        print('使用ip:{}访问出错：{}'.format(proxy, e))
        return {'type': 0, 'proxy': proxy}

# 限制同时进行测试的代理数
async def check_amount(sem, proxy, session):
    async with sem:
        check_result = await check_one(proxy, session)
        return check_result

async def check_main(proxy_list):
    sem = asyncio.Semaphore(600)
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.ensure_future(check_amount(sem, proxy, session)) for proxy in proxy_list]
        check_result = await asyncio.gather(*tasks)
        return check_result

def main(proxy_list):
    loop = asyncio.get_event_loop()
    res = loop.run_until_complete(check_main(proxy_list))
    return res
    # loop.close()


