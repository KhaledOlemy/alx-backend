#!/usr/bin/env python3
"""Task: 0, get page indices based on page number and page size"""


def index_range(page: int, page_size: int) -> tuple:
    """get the number of items in a {page} number with size of {page_size}"""
    return ((page-1) * page_size, page * page_size)
