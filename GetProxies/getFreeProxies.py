'''
    获取不同站免费ip的方法
'''
import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
from Util.getHtml import WebRequest
from Util.ipFormat import IpFormat
from lxml import etree
import re

def source_ip_format(func):
    def inner():
        proxies_list = func()
        format_proxies_list = IpFormat.format_ip(proxies_list)
        return format_proxies_list
    return inner

class GetProxies:
    def __init__(self):
        pass

    @staticmethod
    @source_ip_format
    def get_from_mimiip():
        base_url = 'http://www.mimiip.com/gngao/{}'
        max_page = 3
        proxies_list = list()
        for url in (base_url.format(page) for page in range(1, max_page+1)):
            response = WebRequest.get(url=url, verify_flag=['MimiIp.com'])
            if response:
                proxies_list_ = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\w\W].*<td>(\d+)</td>', response.text)
                proxies_list += proxies_list_
            else:
                continue
        return proxies_list

    @staticmethod
    @source_ip_format
    def get_from_66ip():
        base_url = 'http://www.66ip.cn/nmtq.php?getnum=500&isp=0&anonymoustype=3&start=&ports=&export=&ipaddress=&area=1&proxytype=2&api=66ip'
        response = WebRequest.get(url=base_url, verify_flag=['安小莫提示：匿名提取成功'], response_encoding='gbk')
        if response:
            proxies_list = re.findall(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+)', response.text)
            return proxies_list
        else:
            return list()

    @staticmethod
    @source_ip_format
    def get_from_xici():
        base_url = 'http://www.xicidaili.com/nn/{}'
        max_page = 3
        proxies_list = list()
        for url in (base_url.format(page) for page in range(1, max_page+1)):
            response = WebRequest.get(url, verify_flag=['国内高匿免费HTTP代理IP'], response_encoding='utf-8')
            if response:
                html = etree.HTML(response.text)
                try:
                    ip_list = html.xpath('//*[@id="ip_list"]/tr[position()>1]/td[2]/text()')
                    port_list = html.xpath('//*[@id="ip_list"]/tr[position()>1]/td[3]/text()')
                    proxies_list += list(map(lambda ip, port:'{}:{}'.format(ip, port), ip_list, port_list))
                except:
                    continue
        return proxies_list

    @staticmethod
    @source_ip_format
    def get_from_goubanjia():
        base_url = 'http://www.goubanjia.com/'
        response = WebRequest.get(base_url, verify_flag=['全网代理IP'], response_encoding='utf-8')
        if not response:
            return list()
        html = etree.HTML(response.text)
        proxies_list = list()
        for tr in html.xpath('//tr[contains(@class, "success") or contains(@class, "warning")]'):
            if len(tr) == 0:
                return list()
            if tr.xpath('td[2]/a/text()')[0] == '透明':continue
            else:
                xpath_str = """td[1]//*[not(contains(@style, 'display: none'))
                                        and not(contains(@style, 'display:none'))
                                        and not(contains(@class, 'port'))
                                        ]/text()
                                """
                ip = ''.join(tr.xpath(xpath_str))
                port = tr.xpath('td[1]/span[contains(@class, "port")]/text()')[0]
                proxies_list.append(ip+':'+port)
        return proxies_list

    @staticmethod
    @source_ip_format
    def get_from_kuaidaili():
        base_url = 'https://www.kuaidaili.com/free/inha/{}/'
        max_page = 3
        proxies_list = list()
        for url in [base_url.format(page) for page in range(1, max_page+1)]:
            response = WebRequest.get(url, verify_flag=['快代理'], response_encoding='utf-8')
            if response:
                html = etree.HTML(response.text)
                try:
                    ip_list = html.xpath('//div[@id="list"]/table/tbody/tr/td[1]/text()')
                    port_list = html.xpath('//div[@id="list"]/table/tbody/tr/td[2]/text()')
                    proxies_list += list(map(lambda ip, port:'{}:{}'.format(ip, port),ip_list, port_list))
                except:
                    continue
        return proxies_list

    @staticmethod
    @source_ip_format
    def get_from_coderbusy():
        base_url = 'https://proxy.coderbusy.com/classical/anonymous-type/highanonymous.aspx?page={}'
        max_page = 3
        proxies_list = list()
        for url in [base_url.format(page) for page in range(1, max_page + 1)]:
            response = WebRequest.get(url, verify_flag=['码农代理'], response_encoding='utf-8')
            if response:
                html = etree.HTML(response.text)
                try:
                    ip_list = html.xpath('//table[@class="table"]/tbody/tr/td[3]/@data-ip')
                    port_list = html.xpath('//table[@class="table"]/tbody/tr/td[3]/text()')
                    proxies_list += list(map(lambda ip, port: '{}:{}'.format(ip, port), ip_list, port_list))
                except:
                    continue
        return proxies_list

    @staticmethod
    @source_ip_format
    def get_from_ip3366():
        base_url = 'http://www.ip3366.net/free'
        proxies_list = list()
        response = WebRequest.get(url=base_url, verify_flag=['云代理'], response_encoding='gb2312')
        if response:
            html = etree.HTML(response.text)
            try:
                ip_list = html.xpath('//tbody/tr/td[1]/text()')
                port_list = html.xpath('//tbody/tr/td[2]/text()')
                proxies_list += list(map(lambda ip, port: '{}:{}'.format(ip, port), ip_list, port_list))
            except:
                return list()
        return proxies_list

    @staticmethod
    @source_ip_format
    def get_from_iphai():
        base_url = 'http://www.iphai.com/free/ng'
        response = WebRequest.get(url=base_url, verify_flag=['IP海'], response_encoding='utf-8')
        if response:
            proxies_list = re.findall(r'<td>\s*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s*?</td>[\s\S]*?<td>\s*?(\d+)\s*?</td>',
                                      response.text)
            return proxies_list
        else:
            return list()

    @staticmethod
    @source_ip_format
    def get_from_proxylist():
        base_url = 'https://proxy-list.org/english/search.php?search=CN.anonymous-and-elite&country=CN&type=anonymous-and-elite&port=any&ssl=any'
        response = WebRequest.get(url=base_url, verify_flag=['China'], response_encoding='utf-8', proxies='gfw_proxies')
        if response:
            proxies_list = re.findall(r"Proxy\('(.*?)'\)", response.text)
            return proxies_list
        else:
            return list()

    @staticmethod
    @source_ip_format
    def get_from_gatherproxy():
        base_url = 'http://www.gatherproxy.com/proxylist/country/?c=China'
        response = WebRequest.get(url=base_url, verify_flag=['china proxy'], response_encoding='utf-8', proxies='gfw_proxies')
        if response:
            ip_list = re.findall(r'"PROXY_IP":"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})",', response.text)
            port_list = re.findall(r'"PROXY_PORT":"(.*?)"', response.text)
            if len(ip_list) == len(port_list) and len(ip_list) > 0:
                proxies_list = list(map(lambda ip, port: '{}:{}'.format(ip, int(port, 16)), ip_list, port_list))
                return proxies_list
            else:
                return list()
        return list()

    @staticmethod
    @source_ip_format
    def get_from_5u():
        base_url = 'http://www.data5u.com/free/gngn/index.shtml'
        response = WebRequest.get(url=base_url, verify_flag=['无忧代理'], response_encoding='utf-8')
        if response:
            html = etree.HTML(response.text)
            try:
                ip_list = html.xpath('//ul[@class="l2"]/span[1]/li/text()')
                port_list = html.xpath('//ul[@class="l2"]/span[2]/li/text()')
                proxies_list = list(map(lambda ip, port: '{}:{}'.format(ip, port), ip_list, port_list))
                return proxies_list
            except:
                return list()
        return list()
if __name__ == '__main__':
    gp = GetProxies()
    print(gp.get_from_coderbusy())
    # for i in globals()