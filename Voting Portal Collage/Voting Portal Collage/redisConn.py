"""Basic connection example.
"""

import redis

redisConnection = redis.Redis(
    host='redis-13025.c253.us-central1-1.gce.redns.redis-cloud.com',
    port=13025,
    decode_responses=True,
    username="karan.bhale",
    password="Karan@123",
    db=0
)

if __name__=='__main__':
    success = redisConnection.set('foo', 'bar')
    # True

    result = redisConnection.get('foo')
    print(result)
# >>> bar

