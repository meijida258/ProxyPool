'''
    异步访问验证网站，快速检验ip有效性,返回检验结果
'''
import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
from Util.getConfig import GetConfig
import aiohttp
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