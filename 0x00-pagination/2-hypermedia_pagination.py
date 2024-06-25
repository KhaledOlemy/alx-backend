#!/usr/bin/env python3
"""Task: 2, gets data from csv returns a dictionary containing
the key-value pairs"""
import csv
import math
from typing import List, Dict


def index_range(page: int, page_size: int) -> tuple:
    """get the number of items in a {page} number with size of {page_size}"""
    return ((page-1) * page_size, page * page_size)


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """gets a page from a csv file with page number and page_size"""
        assert type(page) is int
        assert type(page_size) is int
        assert page > 0
        assert page_size > 0
        starting_point, ending_point = index_range(page, page_size)
        csv_lines = self.dataset()
        if starting_point > len(csv_lines):
            return []
        return csv_lines[starting_point: ending_point]

    def get_hyper(self, page: int = 1, page_size: int = 10) -> List[List]:
        """ Gets data from csv and returns structured dictionary"""
        assert type(page) is int
        assert type(page_size) is int
        assert page > 0
        assert page_size > 0
        starting_point, ending_point = index_range(page, page_size)
        csv_lines = self.dataset()
        data = csv_lines[starting_point: ending_point]
        page_output = {}
        page_output["page_size"] = page_size
        page_output["page"] = page
        page_output["data"] = data
        max_pages = math.ceil(len(csv_lines) / page_size)
        if page < max_pages:
            page_output["next_page"] = page + 1
        else:
            page_output["next_page"] = None
        if page == 1:
            page_output["prev_page"] = None
        else:
            page_output["prev_page"] = page - 1
        page_output["total_pages"] = max_pages
        return page_output
