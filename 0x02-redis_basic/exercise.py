#!/usr/bin/env python3
"""
this module contain class Cache that represent redis cache controller.
"""
import redis
import uuid
from typing import Union


class Cache:
    def __init__(self) -> None:
        """constructor method"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        takes a data argument and returns a string.
        The method should generate a random key (e.g. using uuid),
        store the input data in Redis using the random key and return the key.

        Args:
          data : data stored in redis can be str, bytes, int, float.
        Return:
          random_key : string form of uuid.
        """
        random_key = str(uuid.uuid4())
        self._redis.set(random_key, data)
        return random_key
