#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""

import csv
import math
from typing import List, Dict


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            truncated_dataset = dataset[:1000]
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict:
        """
        Method to get a page of data from the
        dataset with hypermedia pagination.
        Args:
            index (int): The index of the item to retrieve.
            page_size (int): The number of items per page.
        Returns:
            dict: A dictionary containing the page
            data and pagination information.
        """
        assert isinstance(index, int) and isinstance(page_size, int)
        assert 0 <= index < len(self.indexed_dataset()) or index is None

        data = []

        next_index = index + page_size

        for i in range(index, next_index):
            if i in self.indexed_dataset():
                data.append(self.indexed_dataset()[i])
            else:
                next_index += 1
                data.append(self.indexed_dataset()[next_index])

        hypermedia_dict = {
            'index': index,
            'data': data,
            'page_size': len(data),
            'next_index': next_index
        }
        return hypermedia_dict
