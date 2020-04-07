

class RedisCacheKey:

    @staticmethod
    def _get_redis_key(target_id, category):
        return f'{category}:{target_id}'

    @classmethod
    def get_referee_key(cls, target_id):
        return cls._get_redis_key(target_id=target_id, category='referee')

    @classmethod
    def get_stadium_key(cls, target_id):
        return cls._get_redis_key(target_id=target_id, category='stadium')
