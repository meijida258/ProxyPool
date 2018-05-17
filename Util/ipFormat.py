import re, base64

class IpFormat:
    def __init__(self):
        pass

    @staticmethod
    def format_ip(ip_list):
        result = []
        if ip_list:
            # 处理[(ip, port)]格式的地址
            if isinstance(ip_list[0], tuple):
                for ip in ip_list:
                    result.append(':'.join(ip))
                return result
            # 处理[ip：port]格式的地址
            elif re.match(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+)', ip_list[0]):
                return ip_list
            else:
                for ip in ip_list:
                    result.append(base64.b64decode(ip).decode())
                return result
        else:
            return list()