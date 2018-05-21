'''
    本地的web服务器，处理其它程序获取代理的请求
    get http://localhost:6324/proxy_get 获取一个有效ip
    get http://localhost:6324/proxy_get?count=m 获取m个有效ip
    get http://localhost:6324/proxy_get?count=m&score=n 获取m个分数大于n的有效ip
'''
import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from http.server import HTTPServer, BaseHTTPRequestHandler# 启动服务函数
import re
from WebApi.apis import get_proxy
import json
import redis

# 自定义处理程序，用于处理HTTP请求
class TestHTTPHandler(BaseHTTPRequestHandler):
    # 处理GET请求
    redis_conn = redis.StrictRedis(host='localhost', port=6379, db=3)
    def do_GET(self):
        # 正则匹配获得请求参数
        try:
            count = int(re.findall(r'/proxy_get\?count=(\d+)', self.path)[0])
        except IndexError:
            count = 1
        try:
            score = int(re.findall(r'/proxy_get\?.*?&score=(\d+)', self.path)[0])
        except IndexError:
            score = -1
        proxies_list = get_proxy(count, redis_conn=self.redis_conn, score=score)
        # 转成json，在编码成utf-8
        proxies_json = json.dumps(proxies_list).encode('utf-8')
        # self.protocal_version = 'HTTP/1.1'  # 设置协议版本
        self.send_response(200)  # 设置响应状态码
        self.send_header('Content-Type', 'application/json')  # 设置响应头
        self.end_headers()
        self.wfile.write(proxies_json)  # 输出响应内容

def start_server(port):
    http_server = HTTPServer(('localhost', int(port)), TestHTTPHandler)
    http_server.serve_forever()  # 设置一直监听并接收请求


# print(type(json.dumps([{'123.1.1.1:123': '12'}, {'192.168.2.100:8081': '99'}])))
start_server(6324)  # 启动服务，监听8000端口