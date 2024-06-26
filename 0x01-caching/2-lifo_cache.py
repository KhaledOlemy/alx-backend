#!/usr/bin/env python3
"""LIFO Caching System"""
from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """LIFO Cache: Store with a maximum number of `MAX_ITEMS`
    and usd LIFO Caching technique, Last In First Out"""
    def __init__(self):
        """Instance initializer"""
        super().__init__()
        self.last_updated_item = None

    def put(self, key, item):
        """Puts key:value pair in cache"""
        if not key or not item:
            return
        if len(self.cache_data.items()) < BaseCaching.MAX_ITEMS:
            self.cache_data[key] = item
        else:
            if self.last_updated_item:
                discarded_key = self.last_updated_item
            else:
                discarded_key = list(self.cache_data.keys())[-1]
            if self.cache_data.get(key):
                self.cache_data[key] = item
            else:
                print("DISCARD:", discarded_key)
                del self.cache_data[discarded_key]
                self.cache_data[key] = item
        self.last_updated_item = key

    def get(self, key):
        """Gets value from cache using key"""
        if key and self.cache_data.get(key):
            return self.cache_data.get(key)
