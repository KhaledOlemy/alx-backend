#!/usr/bin/env python3
"""LFU Caching System"""
from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """LFU Cache: Store with a maximum number of `MAX_ITEMS`
    and use LFU Caching technique, Least Frequency Used"""
    def __init__(self):
        """Instance initializer"""
        super().__init__()
        self.busy_keys = []
        self.historical_keys = []

    def put(self, key, item):
        """Puts key:value pair in cache"""
        if not key or not item:
            return
        if len(self.cache_data.items()) < BaseCaching.MAX_ITEMS:
            self.cache_data[key] = item
            self.busy_keys.append(key)
            self.historical_keys.append(key)
        else:
            if self.cache_data.get(key):
                self.cache_data[key] = item
                self.busy_keys.remove(key)
                self.busy_keys.append(key)
                self.historical_keys.append(key)
            else:
                self.busy_keys = [i for i in self.busy_keys if i in  # ########
                                  list(self.cache_data.keys())]
                self.historical_keys = [i for i in self.historical_keys if i in
                                        list(self.cache_data.keys())]
                indexing = {}
                t = [indexing.update({i: self.historical_keys.count(i)})
                     for i in list(set(self.historical_keys)) if i
                     in self.busy_keys]
                least_freq_occ = min(list(indexing.values()))
                least_freq = [i for i, j in indexing.items() if
                              j == least_freq_occ and i in self.busy_keys]
                if len(least_freq) == 1:
                    discarded_key = least_freq[0]
                else:
                    temp_list = [i for i in self.busy_keys if i in least_freq]
                    discarded_key = temp_list[0]
                print("DISCARD:", discarded_key)
                del self.cache_data[discarded_key]
                self.cache_data[key] = item
                self.busy_keys.append(key)
                self.historical_keys.append(key)

    def get(self, key):
        """Gets value from cache using key"""
        if key and self.cache_data.get(key):
            self.busy_keys.remove(key)
            self.busy_keys.append(key)
            self.historical_keys.append(key)
            return self.cache_data.get(key)
