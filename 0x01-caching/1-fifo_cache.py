#!/usr/bin/env python3
"""FIFO Caching System"""
from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    def __init__(self):
        """Instance initializer"""
        super().__init__()

    def put(self, key, item):
        """Puts key:value pair in cache"""
        if not key or not item:
            return
        if len(self.cache_data.items()) < BaseCaching.MAX_ITEMS:
            self.cache_data[key] = item
        else:
            discarded_key = list(self.cache_data.keys())[0]
            print("DISCARD:", discarded_key)
            del self.cache_data[discarded_key]
            self.cache_data[key] = item

    def get(self, key):
        """Gets value from cache using key"""
        if key and self.cache_data.get(key):
            return self.cache_data.get(key)
