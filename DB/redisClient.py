import redis
from Util.getConfig import GetConfig

class RedisConn:
    def __init__(self):
        self.redis_conn = redis.StrictRedis(host='localhost', port=6379, db=3)

    def push_hash(self, hash_name, proxy_dict):
        '''
        :param hash_name:
        :param proxy_dict: {proxy:score}
        :return:
        '''
        return self.redis_conn.hmset(hash_name, proxy_dict)

    def del_hash(self, hash_name, key):
        return self.redis_conn.hdel(hash_name, key)

    def get_all_hash(self, hash_name):
        '''
        :param hash_name:
        :return: 编码过的ip列表
        '''
        return [key.decode('utf-8') for key in self.redis_conn.hgetall(hash_name).keys()]


if __name__ == '__main__':
    rc = RedisConn()
    rc.push_hash('UsefulProxy', {'192.168.2.100:8081':99})
    # rc.redis_conn.rpush('123',1,1,1)

