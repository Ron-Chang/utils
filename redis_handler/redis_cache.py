

class RedisCache:

    redis_instance = None

    @classmethod
    def import_redis(cls, redis_instance):
        cls.redis_instance = redis_instance

    @classmethod
    def set_cache(cls, key, value, expire_time=60 * 60 * 24 * 14):
        cls.redis_instance.set(key, value, ex=expire_time)

    @classmethod
    def get_cache(cls, key):
        value = cls.redis_instance.get(key)
        if value:
            cls.set_cache(key=key, value=value)
        return value
