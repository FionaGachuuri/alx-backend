#!/usr/bin/env python3
"""
Module to paginate a database of popular baby names.
"""
import csv
import math
from typing import List


def index_range(page: int, page_size: int) -> tuple:
    """Calculate the start and end index for a given page and page size.

    Args:
        page (int): The page number.
        page_size (int): The number of items per page.

    Returns:
        tuple: A tuple containing the start and end index.
    """
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    return start_index, end_index


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
        """
        Method to get a page of data from the dataset.
        Args:
            page (int): The page number to retrieve.
            page_size (int): The number of items per page.
        Returns:
            List[List]: A list of lists representing
            the data on the requested page.
        """
        assert isinstance(page, int) and page > 0
        assert isinstance(page_size, int) and page_size > 0
        dataset_length = len(self.dataset())
        start, end = index_range(page, page_size)
        if start >= dataset_length:
            return []
        if end > dataset_length:
            end = dataset_length
        return self.dataset()[start:end]

    def get_hyper(self, page: int = 1, page_size: int = 10) -> dict:
        """
        Method to get a page of data from the
        dataset with hypermedia pagination.
        Args:
            page (int): The page number to retrieve.
            page_size (int): The number of items per page.
        Returns:
            dict: A dictionary containing the page data
            and pagination information.
        """
        assert isinstance(page, int) and page > 0
        assert isinstance(page_size, int) and page_size > 0
        retrieved_dataset = self.get_page(page, page_size)

        hypermedia_dict = {
            'page_size': len(retrieved_dataset),
            'page': page,
            'data': retrieved_dataset,
            'next_page': page + 1 if len(retrieved_dataset)
            == page_size else None,
            'prev_page': page - 1 if page > 1 else None,
            'total_pages': math.ceil(len(self.dataset()) / page_size)
        }
        return hypermedia_dict
