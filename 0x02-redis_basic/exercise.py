#!/usr/bin/env python3
"""
this module contain class Cache that represent redis cache controller.
"""
import redis
import uuid
from typing import Union, Callable, Optional, Any
from functools import wraps


def count_calls(func: Callable) -> Callable:
    """
    decorator function that count the number of times func stores.
    """
    @wraps(func)
    def wrapper(self, *args, **kwargs) -> Any:
        """
        wrapper function that return the output of func.
        """
        if self._redis.get(func.__qualname__) is None:
            self._redis.set(func.__qualname__, 1)
        else:
            self._redis.incr(func.__qualname__)
        return func(self, *args, **kwargs)

    return wrapper


class Cache:
    def __init__(self) -> None:
        """constructor method"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
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

    def get(self, key: str, fn: Optional[Callable] = None) -> Any:
        """
        take a key string argument and an optional Callable argument named fn.
        This callable will be used to convert the data back
        to the desired format.
        Args:
          key : str.
          fn : callable to return desired datatype
        Return:
          value : can be any type according to fn.
        """
        value = self._redis.get(key)
        if value is None:
            return None
        if fn:
            return fn(value)
        return value

    def get_str(self, key: str) -> Optional[str]:
        """
        convert bytes to str
        Args:
          key : str.
        Return:
          value : string represent value of key in redis.
        """
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> Optional[int]:
        """
        convert bytes to int
        Args:
          key : str.
        Return:
          value : int represent value of key in redis.
        """
        return self.get(key, lambda x: int(x.decode('utf-8')))
