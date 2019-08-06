#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:10521
# datetime:2019-08-06 23:28
# software: PyCharm

import redis
from config import settings


class Redis(object):

    def __init__(self, host='', port='', password='', db='') -> None:
        super(Redis).__init__()
        try:
            redis_connector = redis.Redis(
                host=host or settings.redis['HOST'],
                port=port or settings.redis['POST'],
                password=password or settings.redis['PASSWORD'],
                db=db or settings.redis['DB'],
                decode_responses=True
            )
            self.redis = redis_connector
        except Exception as connection_error:
            print('redis连接出现异常:', connection_error)


Redis = Redis()
