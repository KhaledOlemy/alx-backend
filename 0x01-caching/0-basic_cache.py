#!/usr/bin/env python3
"""Basic Caching System"""
from base_caching import BaseCaching


class BasicCache(BaseCaching):
    """Basic Caching System"""
    def put(self, key, item):
        """Puts key:value pair in cache"""
        if key and item:
            self.cache_data[key] = item

    def get(self, key):
        """Gets value from cache using key"""
        if key and self.cache_data.get(key):
            return self.cache_data[key]
