# -*- coding: utf-8 -*-
"""
Created on Thu Aug 23 17:29:09 2018

@author: tony.zhao2
"""

import pandas as pd
from pandas.core.groupby.groupby import DataError
from pandas.errors import EmptyDataError
import ParseData


class Signal_of_one_file(object):
    def __init__(self):
        self._data = pd.DataFrame()

    def add_file(self, file_path):
        self._data = self._data.append(ParseData.parse_file(file_path))

    def get_CE(self):
        return self._data.index.unique(level='CE').values[0]


if __name__ == "__main__":
    filepath = '922-230\graph_0012.txt'
    signal = Signal_of_one_file()
    signal.add_file(filepath)