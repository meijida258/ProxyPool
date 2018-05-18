'''
    封住requests的get请求，方便使用
'''
import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
from Util.getUserAgent import FakeChromeUA
import requests
import time

class WebRequest:
    def __init__(self):
        self.gfw_proxies = '192.168.2.100:8081'

    def headers(self):
        user_agent = FakeChromeUA.get_ua()
        return {'User-Agent': user_agent,
                'Accept': '*/*',
                'Connection': 'keep-alive',
                'Accept-Language': 'zh-CN,zh;q=0.8'}
    @staticmethod
    def get(url, retry_times=5, proxies=None, timeout=30, interval=3, verify_flag=list(), response_encoding=None):
        # 是否使用代理
        if proxies == 'gfw_proxies':
            used_proxies = {'http': 'http://{}'.format(wr.gfw_proxies),
                            'https': 'http://{}'.format(wr.gfw_proxies)}
        elif proxies:
            used_proxies = {'http':'http://{}'.format(proxies)}
        else:
            used_proxies = {}

        while retry_times > 0:
            try:
                response = requests.get(url, proxies=used_proxies, headers=wr.headers(), timeout=timeout)
                if response_encoding:
                    response.encoding = response_encoding
                if any(f in response.text for f in verify_flag):
                    print('获取页面{}成功'.format(url))
                    return response
                else:
                    raise Exception
            except Exception as e:
                print(e.args)
                retry_times -= 1
                if retry_times == 0:
                    print('获取页面{}失败'.format(url))
                    return None

                time.sleep(interval)

if __name__ == '__main__':
    wr = WebRequest()
else:
    wr = WebRequest()