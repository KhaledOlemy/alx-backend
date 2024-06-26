#!/usr/bin/env python3
"""MRU Caching System"""
from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """MRU Cache: Store with a maximum number of `MAX_ITEMS`
    and usd MRU Caching technique, First In First Out"""
    def __init__(self):
        """Instance initializer"""
        super().__init__()
        self.busy_keys = []

    def put(self, key, item):
        """Puts key:value pair in cache"""
        if not key or not item:
            return
        if len(self.cache_data.items()) < BaseCaching.MAX_ITEMS:
            self.cache_data[key] = item
            self.busy_keys.append(key)
        else:
            discarded_key = self.busy_keys.pop()
            if self.cache_data.get(key):
                self.cache_data[key] = item
                self.busy_keys.append(key)
            else:
                print("DISCARD:", discarded_key)
                del self.cache_data[discarded_key]
                self.cache_data[key] = item
                self.busy_keys.append(key)

    def get(self, key):
        """Gets value from cache using key"""
        if key and self.cache_data.get(key):
            self.busy_keys.append(key)
            return self.cache_data.get(key)
