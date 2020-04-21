"""
This file has all the redis connection settings
Author: Akshaya Revaskar
Date: 12/04/2020
"""
import redis
import logging
import os
logging.basicConfig(level=logging.DEBUG)
from dotenv import load_dotenv

load_dotenv()


class RedisService:
    def __init__(self, host=os.getenv("flask_redis_host"), port=os.getenv("flask_redis_port"),
                 db=os.getenv("flask_redis_db"), ):
        self.host = host
        self.port = port
        self.db = db
        self.connection = self.connect()

    def connect(self):
        connection = redis.StrictRedis(host=self.host, port=self.port, db=self.db)
        if connection:
            logging.info('Redis Cache Connection established')
        return connection

    # function for setting data into redis
    def set(self, key, value, exp_s=None, exp_ms=None):
        self.connection.set(key, value, exp_s, exp_ms)
        logging.info(f'{key} : {value}')

    # function for getting data from redis
    def get(self, key):
        return self.connection.get(key)

    # function for checking whether data exists
    def exists(self, key):
        return self.connection.exists(key)

    # function for deleting data from redis
    def delete(self, key):
        logging.info(f'Key to Delete : {key}')
        self.connection.delete(key)