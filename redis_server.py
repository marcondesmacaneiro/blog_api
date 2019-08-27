import datetime
from datetime import timedelta
from time import strftime

import redis


ACCESS_EXPIRES = timedelta(minutes=15)
REFRESH_EXPIRES = timedelta(days=30)
revoked_store = redis.StrictRedis(host='localhost', port=6379, db=0,
                                  decode_responses=True)
