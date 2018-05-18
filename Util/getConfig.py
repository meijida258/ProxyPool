'''
    读取config文件
'''
from configparser import ConfigParser
import os

class GetConfig:
    def __init__(self):
        self.config_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + os.sep + 'Config.ini'
        self.config = ConfigParser()
        self.config.read(self.config_path)

    def get_proxy_func(self):
        used_proxy_funcs = list()
        func_items = self.config['GETPROXYFUNCS'].items()
        for func in func_items:
            if func[1] == '1':
                used_proxy_funcs.append(func[0])
        return used_proxy_funcs



if __name__ == '__main__':
    gc = GetConfig()
else:
    gc = GetConfig()