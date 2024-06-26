#!/usr/bin/env python3
"""Basic Caching System"""
from base_caching import BaseCaching


class BasicCache(BaseCaching):
    """Basic Caching System"""
    def put(self, key, item):
        """Puts key:value pair in cache"""
        self.cache_data[key] = item

    def get(self, key):
        """Gets value from cache using key"""
        return self.cache_data[key]
