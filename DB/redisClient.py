'''
    连接redis，以及相关操作
'''
import redis

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

    def get_all_hash(self, hash_name, result_type=1):
        '''
        :param hash_name:
        :param result_type: 返回的格式:1-仅返回ip的列表 2-返回{ip:score}的列表
        :return:
        '''
        if result_type == 1:
            return [key.decode('utf-8') for key in self.redis_conn.hgetall(hash_name).keys()]
        elif result_type == 2:
            return [{key.decode('utf-8'):value.decode('utf-8')} for key, value in self.redis_conn.hgetall(hash_name).items()]

if __name__ == '__main__':
    rc = RedisConn()
    # rc.push_hash('123123', {'192.168.2.100:8081':99}

    # rc.redis_conn.rpush('123',1,1,1)

