'''
    随机获取ua
'''
import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
import random

__all__ = ['FakeChromeUA']

FIRST_NUM = random.randint(55, 62)
THIRD_NUM = random.randint(0, 3200)
FOURTH_NUM = random.randint(0, 140)


class FakeChromeUA:
    """Fake UA Factory"""
    os_type = [
        '(Windows NT 6.1; WOW64)', '(Windows NT 10.0; WOW64)',
        '(X11; Linux x86_64)',
        '(Macintosh; Intel Mac OS X 10_12_6)'
    ]

    chrome_version = 'Chrome/{}.0.{}.{}'.format(FIRST_NUM, THIRD_NUM, FOURTH_NUM)

    @classmethod
    def get_ua(cls):
        """return fack ua"""
        return ' '.join(
            ['Mozilla/5.0', random.choice(cls.os_type),
             'AppleWebKit/537.36',
             '(KHTML, like Gecko)',
             cls.chrome_version, 'Safari/537.36'])
if __name__ == '__main__':
    fc = FakeChromeUA()
